# pynpm-download - A Js Dependency Downloader using NPM Public Registry API

## Usage

```python
from pynpmd import JsLibResolver

libs = ["d3", "@hpcc-js/wasm"]
rsvr = JsLibResolver()
for lib in libs:
   print(rsvr.get_lib(lib))
```

## FAQ

### Whats the difference to other approaches?

Most other libaries are either bound to a certain Web-framework or use npm binary. This library only uses the web api.

### Why don't you use Google Hosed Libraries (or similar) to get external js-libraries?

- GDPR (If there is no other server, you do not have to point it out in the privacy policy.)
- It works locally with bad or no internet connection (after inital download).