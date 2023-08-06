# -*- coding: utf-8 -*-
"""
    sphinxcontrib.plot
    ~~~~~~~~~~~~~~~~~~~~~

    Allow plot commands be rendered as nice looking images
    

    See the README file for details.

    :author: Vadim Gubergrits <vadim.gubergrits@gmail.com>
    :license: BSD, see LICENSE for details

    Inspired by ``sphinxcontrib-aafig`` by Leandro Lucarella.
"""

import re, os
import posixpath
from os import path
import shutil
import copy
from subprocess import Popen, PIPE
import shlex
import imghdr

try:
    # Python 2.
    from StringIO import StringIO
    # Python 3.
except ImportError:
    from io import StringIO

try:
    from hashlib import sha1 as sha
except ImportError:
    from sha import sha

from docutils import nodes
from docutils.parsers.rst import Directive, directives
from sphinx.errors import SphinxError
from sphinx.util import ensuredir, relative_uri

OUTPUT_DEFAULT_FORMATS = dict(html='svg', latex='pdf', text=None)
OWN_OPTION_SPEC = dict( { 'caption': str,
    'size': str,
    'plot_format': str,
    'convert': str,
    'show_source': str,
    })

class PlotError(SphinxError):
    category = 'plot error'

class PlotDirective(directives.images.Figure):
    """
    Directive that builds figure object.
    """
    has_content = True
    required_arguments = 0
    option_spec = directives.images.Figure.option_spec.copy()
    option_spec.update(OWN_OPTION_SPEC)
  
    def run(self):
        self.arguments = ['']
        total_options = self.options.copy()

        cmd = self.content[0]
        text = '\n'.join(self.content[1:])
        own_options = dict([(k,v) for k,v in self.options.items() 
                                  if k in OWN_OPTION_SPEC])

        # Remove the own options from self-options which will be as figure
        # options.
        for x in own_options.keys():
            self.options.pop(x)

        # don't parse the centent as legend, it's not legend.
        self.content = None

        (node,) = directives.images.Figure.run(self)
        if isinstance(node, nodes.system_message):
            return [node]

        node.plot = dict(cmd=cmd,text=text,options=own_options,suffix="plot",
                directive="plot", total_options=total_options)
        return [node]

# http://epydoc.sourceforge.net/docutils/
def render_plot_images(app, doctree):

    for fig in doctree.traverse(nodes.figure):
        if not hasattr(fig, 'plot'):
            continue

        cmd = fig.plot['cmd']
        text = fig.plot['text']
        options = fig.plot['options']

        try:
            #relfn, outfn, relinfile = cmd_2_image(app, fig.plot)
            out = cmd_2_image(app, fig.plot)
            caption_node = nodes.caption("", options.get("caption", cmd))
            fig += caption_node
            fig['ids'] = "plot"
            #img = fig.children[fig.first_child_matching_class(nodes.image)]
            for img in fig.traverse(condition=nodes.image):
                img['uri'] = out["outrelfn"]
                if out["outreference"]:
                    reference_node = nodes.reference(refuri=out["outreference"])
                    reference_node += img
                    fig.replace(img, reference_node)
                #img['candidates']={'*': out["outfullfn"]}

            #if options.get("show_source", False):
            #    # rendere as a text
            #    fig["align"] = "left"
            #    fig.insert(0, nodes.literal_block("", "%s\n%s" %(cmd, text), align = "left"))
            #print("rending figure: %s" %(fig))
        except PlotError as err:
            #app.builder.warn('plot error: ')
            print(err)
            fig.replace_self(nodes.literal_block("", "%s\n%s" %(cmd, text)))
            continue

    for img in doctree.traverse(nodes.image):
        if not hasattr(img, 'plot'):
            continue

        text = img.plot['text']
        options = img.plot['options']
        cmd = img.plot['cmd']
        try:
            #relfn, outfn, relinfile = cmd_2_image(app, img.plot)
            out = cmd_2_image(app, img.plot)
            img['uri'] = out["outrelfn"]
            if out["outreference"]:
                reference_node = nodes.reference(refuri=out["outreference"])
                img.replace_self(reference_node)
                reference_node.append(img) 
            #if options.get("show_source", False):
            #    img.insert(0, nodes.literal_block("", "%s\n%s" %(cmd, text)))
        except PlotError as err:
            #app.builder.warn('plot error: ')
            print(err)
            img.replace_self(nodes.literal_block("", "%s\n%s" %(cmd, text)))
            continue

def cmd_2_image (app, plot):
    """Render plot code into a PNG output file."""
    #print("app.builder.format: %s" %(app.builder.format))
    #print("app.builder.env.docname: %s" %(app.builder.env.docname))
    #print("app.builder.imagedir: %s" %(app.builder.imagedir))

    cmd = plot['cmd']
    args = shlex.split(cmd)
    text = plot['text']
    options = plot['options']
    format = app.builder.format
    rel_imgpath = relative_uri(app.builder.env.docname, app.builder.imagedir)
    hashkey = cmd + str(options) + text
    hashkey = sha(hashkey.encode('utf-8')).hexdigest()
    infname = '%s-%s.%s' % (args[0], hashkey, plot['suffix'])
    infullfn = path.join(app.builder.outdir, app.builder.imagedir, infname)
    ensuredir(path.join(app.builder.outdir, app.builder.imagedir))
    currpath = os.getcwd() # Record the current dir and return here afterwards

    if options.get("plot_format", None): #User definition is higher priority.
        plot_format = options["plot_format"]
    else:
        format_map = OUTPUT_DEFAULT_FORMATS.copy()
        format_map.update(app.builder.config.plot_output_format)
        plot_format = format_map.get(app.builder.format, "png")
    # convert only support png.
    plot_format = options.get("convert", None) and "png" or plot_format

    outfname = '%s-%s.%s' %(args[0], hashkey, plot_format)
    out = dict(outrelfn = posixpath.join(rel_imgpath, outfname),
        outfullfn = path.join(app.builder.outdir, app.builder.imagedir, outfname),
        #outreference = posixpath.join(rel_imgpath, infname),
        outreference = None)
    #print(out)

    if path.isfile(out["outfullfn"]):
        print("file has already existed: %s" %(outfname))
        return out
    if "ditaa" in cmd:
        if plot_format in ["svg", "pdf"]:
            cmd += " --svg" #ditaa support vector image by --svg parameter.
        args.extend([infname, outfname])
        # Ditaa must work on the target directory.
        os.chdir(path.join(app.builder.outdir, app.builder.imagedir))
    elif args[0] == "dot":
        # dot -Tpng in_file -o out_file
        args.extend([infullfn, '-o', out["outfullfn"]])
    elif "python" in args[0]:
        pylib = "pyplot"
        lines = StringIO(text).readlines()
        for l in lines:
            if (not l.lstrip().startswith('#')) and ("import matplotlib.pyplot" in l):
                # Find out pyplot module name, use pyplot if not found.
                result = re.search("(?<=import matplotlib.pyplot as )\w+", l, flags=0)
                pylib = result and result.group() or "pyplot"
            elif ('.show()' in l or 'savefig(' in l):
                lines.remove(l)
        lines.append('%s.savefig("%s")\n' %(pylib, out["outfullfn"]))
        text = ''.join(lines)
        args.append(infullfn)
        #print("text: %s, pylib: %s" %(text, pylib))
    elif args[0] == "gnuplot":
        size = options.get("size", "900,600")
        if (plot_format in ["pdf", "eps"] and "," in options["size"]):
            # pdf unit is inch while png is pixel, convert them.
            tmp = map(lambda x: int(x.strip())/100, options["size"].split(","))
            size = ",".join("%d"%(i) for i in tmp)

        lines = StringIO(text).readlines()
        for l in lines: # reset the output/terminal lines
            if ('set\s+output' in l or 'set\s+term' in l):
                lines.remove(l)
        lines.insert(0, 'set output "%s"\n' %(out["outfullfn"]))
        lines.insert(0, 'set terminal %s size %s\n' %(plot_format, size))
        text = ''.join(lines)
        #print("text: %s" %(text))

        args.append(infullfn)
    elif args[0] == "convert":
        # Attach the body and change the embeded output file.
        if text:
            for i in StringIO(text).readlines():
                args.extend(shlex.split(i.rstrip("\r\n\\")))
        args[-1] = out["outfullfn"]
    else:
        args.append(infullfn)

    #print("text: %s" %(text))
    # write the text as infile.
    with open(infullfn, 'wb') as f:
        f.write(text.encode('utf-8'))

    # 2) generate the output file
    try:
        print(' '.join(args))
        p = Popen(args, stdout=PIPE, stdin=PIPE, stderr=PIPE)
        stdout, stderr = (p.stdout.read().decode("utf-8"),
                p.stderr.read().decode("utf-8"))
        print("[31m%s[1;30m%s[0m" %(stderr, stdout))
    except OSError as err:
        os.chdir(currpath)
        raise PlotError('[1;31m%s[0m' %(err))

    # We'd like to change something after image is generated:
    if options.get("convert", None):
        c = "convert %s" %(out["outfullfn"])
        for i in StringIO(options["convert"]).readlines():
            if (i.lstrip()[0] != "#"):
                c += " %s" %(i.strip().rstrip("\\"))
        c += " %s" %(out["outfullfn"])
        print(c)
        os.system(c)
    if (args[0] == "ditaa") and (plot_format in ['pdf']):
        # In fact ditaa don't support pdf, we convert the .svg to .pdf.
        print("mv %s %s-%s.svg" %(outfname, args[0], hashkey))
        os.system("mv %s %s-%s.svg" %(outfname, args[0], hashkey))
        print("inkscape -f %s-%s.svg -A %s" %(args[0], hashkey, out["outfullfn"]))
        os.system("inkscape -f %s-%s.svg -A %s" %(args[0], hashkey, out["outfullfn"]))


    # 3) Check if it's need to generate the outreference file
    if options.get("show_source", False):
        # Input file could be rendered as a link
        out["outreference"] = posixpath.join(rel_imgpath, infname)

    os.chdir(currpath)
    return out

def setup(app):
    app.add_directive('plot', PlotDirective)
    app.connect('doctree-read', render_plot_images)
    app.add_config_value('plot', 'plot', 'html')
    app.add_config_value('plot_args', [], 'html')
    app.add_config_value('plot_log_enable', True, 'html')
    app.add_config_value('plot_output_format', OUTPUT_DEFAULT_FORMATS, 'html')

#https://blog.csdn.net/wangchaoqi1985/article/details/80461850
