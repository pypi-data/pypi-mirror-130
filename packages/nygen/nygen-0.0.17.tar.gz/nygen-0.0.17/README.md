# nygen

Easily create new python projects

## Usage

`nygen init --author "Natalie Fearnley" --email "nfearnley@gmail.com" --github "nfearnley"`

`cd c:\users\nfear\Desktop\coding`

`nygen myproject`

## Templates

### Usage

Templates can be specified using the `--template` option.

`nygen myproject --template mytemplate`

The default template is "default".

### Creation

Templates can be created by publishing a package that creates an entry point "nygen.templates" that points to the template's data directory.

Example from a setup.cfg file:

```
[options.entry_points]
nygen.templates =
    default = nygen_default.template
```

You can use the [nygen_default](https://github.com/nfearnley/nygen_default) repo as an example of a working template package.
