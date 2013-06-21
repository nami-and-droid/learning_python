import conv_ini
import conv_json


def ini_to_json(fname):
    ext = '.ini'
    fl = open((fname[:-len(ext)] if fname.endswith(ext) else fname)
              + ".json", 'w')
    fl.writelines(conv_json.generate(conv_ini.parse(fname)))
