# modulesbuilder

A build tools package for [Environment Modules](http://modules.sourceforge.net/) written in Python.

This package is the base of a build system for Environment Modules. Each Module is defined with a YAML configuration file. The Module software is built using Docker, and a Modulefile is generated based on the configuration.

```
import modulesbuilder as mb
mb.build(...)
```

Copyright and License are covered by LICENSE.txt.
