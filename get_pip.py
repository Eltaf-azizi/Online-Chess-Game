import os.path
import pkgutil
import shutil
import sys
import struct
import tempfile


PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3


if PY3:
    iterbytes = iter
else:
    def iterbytes(buf):
        return (ord(byte) for byte in buf)


try:
    from base64 import b85decode
except ImportError:
    _b85alphabet = (b"0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                    b"abcdefghijklmnopqrstuvwxyz!#$%&()*+-;<=>?@^_`{|}~")



    def b85decode(b):
        _b85dec = [None] * 256
        for i, c in enumerate(iterbytes(_b85alphabet)):
            _b85dec[c] = i

        padding = (-len(b)) % 5
        b = b + b'~' * padding
        out = []
        packI = struct.Struct('!I').pack
        for i in range(0, len(b), 5):
            chunk = b[i:i + 5]
            acc = 0
            try:
                for c in iterbytes(chunk):
                    acc = acc * 85 + _b85dec[c]
            except TypeError:
                for j, c in enumerate(iterbytes(chunk)):
                    if _b85dec[c] is None:
                        raise ValueError(
                            'bad base85 character at position %d' % (i + j)
                        )
                raise
            try:
                out.append(packI(acc))
            except struct.error:
                raise ValueError('base85 overflow in hunk starting at byte %d'
                                 % i)

        result = b''.join(out)
        if padding:
            result = result[:-padding]
        return result



def bootstrap(tmpdir=None):
    import pip._internal
    from pip._internal.commands.install import InstallCommand
    from pip._internal.req.constructors import install_req_from_line

    
    class CertInstallCommand(InstallCommand):
        def parse_args(self, args):
    
            if not self.parser.get_default_values().cert:
                self.parser.defaults["cert"] = cert_path 
            return super(CertInstallCommand, self).parse_args(args)

    pip._internal.commands_dict["install"] = CertInstallCommand

    implicit_pip = True
    implicit_setuptools = True
    implicit_wheel = True

    if "--no-setuptools" in sys.argv or os.environ.get("PIP_NO_SETUPTOOLS"):
        args = [x for x in sys.argv[1:] if x != "--no-setuptools"]
        implicit_setuptools = False
    else:
        args = sys.argv[1:]

    if "--no-wheel" in args or os.environ.get("PIP_NO_WHEEL"):
        args = [x for x in args if x != "--no-wheel"]
        implicit_wheel = False


    if implicit_setuptools:
        try:
            import setuptools  # noqa
            implicit_setuptools = False
        except ImportError:
            pass
    if implicit_wheel:
        try:
            import wheel  # noqa
            implicit_wheel = False
        except ImportError:
            pass


    for arg in args:
        try:
            req = install_req_from_line(arg)
        except Exception:
            continue

        if implicit_pip and req.name == "pip":
            implicit_pip = False
        elif implicit_setuptools and req.name == "setuptools":
            implicit_setuptools = False
        elif implicit_wheel and req.name == "wheel":
            implicit_wheel = False

    
    if implicit_pip:
        args += ["pip"]
    if implicit_setuptools:
        args += ["setuptools"]
    if implicit_wheel:
        args += ["wheel"]

    
    args = ["install", "--upgrade", "--force-reinstall"] + args

    delete_tmpdir = False
    try:
        
        if tmpdir is None:
            tmpdir = tempfile.mkdtemp()
            delete_tmpdir = True

        
        cert_path = os.path.join(tmpdir, "cacert.pem")
        with open(cert_path, "wb") as cert:
            cert.write(pkgutil.get_data("pip._vendor.certifi", "cacert.pem"))

        
        sys.exit(pip._internal.main(args))
    finally:
        
        if delete_tmpdir and tmpdir:
            shutil.rmtree(tmpdir, ignore_errors=True)


def main():
    tmpdir = None
    try:
        
        tmpdir = tempfile.mkdtemp()

        
        pip_zip = os.path.join(tmpdir, "pip.zip")
        with open(pip_zip, "wb") as fp:
            fp.write(b85decode(DATA.replace(b"\n", b"")))

       
        sys.path.insert(0, pip_zip)

        
        bootstrap(tmpdir=tmpdir)
    finally:
        
        if tmpdir:
            shutil.rmtree(tmpdir, ignore_errors=True)




if __name__ == "__main__":
    main()