#!/usr/bin/env python

import re
from enum import Enum
from collections import defaultdict

SourceParts = Enum('SourceParts', 'folder vcs url fragment')


class SRCINFO:
    def __init__(self, filepath=None, content=None):
        """
        Parses and holds data of a .SRCINFO file.
        ;param filepath: Path to a .SRCINFO file
        ;param content: Content of a .SRCINFO file as string
        Access the data with the object 'content'
        """
        return_dict = defaultdict(list)

        if filepath:
            file = open(filepath, 'r')
        else:
            file = content.splitlines(keepends=True)

        for line in file:
            if line.startswith("#") or line == "\n":  # ignore commented or empty lines
                continue
            line = line.replace('\n', '')  # remove newlines and tabs
            line = line.replace('\t', '')
            array = line.split(" = ")
            key = array[0]
            value = array[1]
            if not return_dict.get(key):
                return_dict[key] = value  # set new value
            else:
                if not type(return_dict[key]) is list:
                    return_dict[key] = [return_dict[key], value]  # convert value to array and append
                else:
                    return_dict[key].append(value)  # append to array
        self.content = return_dict

    def getcontent(self):
        return self.content

    def getrundeps(self):
        rundeps = self.getcontent().get('depends')
        return rundeps if not rundeps is None else []

    def getmakedeps(self):
        makedeps = self.getcontent().get('makedepends')
        return makedeps if not makedeps is None else []

    def getcheckdeps(self):
        checkdeps = self.getcontent().get('checkdepends')
        return checkdeps if not checkdeps is None else []


def parse_source_field(source_text, source_parts):
    """
    Parse the source text from PKGBUILD or .SRCINFO file and return desired parts
    :param source_text: The text (see https://wiki.archlinux.org/index.php/VCS_package_guidelines#VCS_sources)
    :param source_parts: Which part to return; use the SourceParts enum
    """
    if not type(source_parts) is SourceParts:
        return None
    if source_parts is SourceParts.folder:
        if "::" in source_text:
            # return source_text.split("::")[0]
            return re.search('(.+?)::', source_text).group(1)
        return None
    elif source_parts is SourceParts.vcs:
        if "+" in source_text:
            return re.search('(?:.*::)?(.+?)\+', source_text).group(1)
    elif source_parts is SourceParts.url:
        if "#" in source_text:
            return re.search('(?:.*\+)?(.+?)#', source_text).group(1)  # TODO: Make simpler without if
        return re.search('(?:.*\+)?(.*)', source_text).group(1)
    elif source_parts is SourceParts.fragment:
        if "#" in source_text:
            return re.search('#(.*)', source_text).group(1)

if __name__ == '__main__':
    # srcinfo = SRCINFO(sys.argv[1])
    # print(json.dumps(srcinfo.content))
    print(parse_source_field("git+http://project_url#branch=project_branch", SourceParts.folder))
    print(parse_source_field("project_name::git+http://project_url#branch=project_branch", SourceParts.vcs))
    print(parse_source_field("project_name::git+http://project_url", SourceParts.url))
    print(parse_source_field("project_name::git+http://project_url", SourceParts.fragment))
    print(parse_source_field("project_name::git+http://project_url#branch=project_branch", SourceParts.fragment))
