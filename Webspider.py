
import re
import os


class tag_obj:
    def __init__(self):
        self.pos = 0
        self.name = ""
        self.class_name = ""
        self.content = ''
        self.children =''
        self.pairpos = -1
        self.pair=""
        self.tag_label = ""


class spider:
    def __init__(self, txt):
        self.html = txt
        self.tag_scope = [
            "!DOCTYPE",
            "a",
            "abbr",
            "acronym",
            "address",
            "applet",
            "area",
            "article",
            "aside",
            "audio",
            "b",
            "base",
            "basefont",
            "bdi",
            "bdo",
            "big",
            "blockquote",
            "body",
            "br",
            "button",
            "canvas",
            "caption",
            "center",
            "cite",
            "code",
            "col",
            "colgroup",
            "command",
            "datalist",
            "dd",
            "del",
            "details",
            "dir",
            "div",
            "dfn",
            "dialog",
            "dl",
            "dt",
            "em",
            "embed",
            "fieldset",
            "figcaption",
            "figure",
            "fig",
            "font",
            "footer",
            "form",
            "frame",
            "frameset",
            "h1",
            "h2",
            "h3",
            "h4",
            "h5",
            "h6",
            "head",
            "header",
            "hr",
            "html",
            "i",
            "iframe",
            "img",
            "input",
            "ins",
            "isindex",
            "kbd",
            "keygen",
            "label",
            "legend",
            "li",
            "link",
            "map",
            "mark",
            "menu",
            "menuitem",
            "meta",
            "meter",
            "nav",
            "noframes",
            "noscript",
            "object",
            "ol",
            "optgroup",
            "option",
            "output",
            "p",
            "param",
            "pre",
            "progress",
            "q",
            "rp",
            "rt",
            "ruby",
            "s",
            "samp",
            "script",
            "section",
            "select",
            "small",
            "source",
            "span",
            "strike",
            "strong",
            "style",
            "sub",
            "summary",
            "sup",
            "table",
            "tbody",
            "td",
            "textarea",
            "tfoot",
            "th",
            "thead",
            "time",
            "title",
            "tr",
            "track",
            "tt",
            "u",
            "ul",
            "var",
            "video",
            "wbr",
            "xmp",
        ]
        self.tag_items = []
        self.tag_items_l = []
        self.tag_items_s = []
        self.get_tag_items()
        self.pos_list = []
        self.tag_list = []
        self.tag_set()
        print("finish set up")
        # find all tag in html, return a tag item list without tag contents

    def get_tag_items(self):
        tagpa = "<(?:"
        for each in self.tag_scope:
            tagpa += each
            if each != self.tag_scope[-1]:
                tagpa += "|"
        # for tag with description
        tagpa1 = tagpa + ")\s.*?>"
        # for tag without descirption
        tagpa2 = tagpa + ")>"
        pa1 = re.compile(tagpa1)
        pa2 = re.compile(tagpa2)
        tag1 = re.findall(pa1, self.html)
        tag2 = re.findall(pa2, self.html)
        self.tag_items_l = tag1
        self.tag_items_s = tag2
        self.tag_items = self.tag_items_l + self.tag_items_s

    # define a method which can be used internally, to avoid error caused by wrong tag_item
    def get_tag_pos(self, tag_label, pos):
        # find tag_item postion, and update in self.tag
        start_pos = pos
        find_result = 0
        str = self.html
        while find_result != -1:
            find_result = str.find(tag_label, start_pos)
            # find tag_label in Html
            if find_result != -1:
                # if found, check whether in pos list. if it is in, update the start position and continue. if not in pos list, update pos list and return position.
                try:
                    self.pos_list.index(find_result)
                except ValueError:
                    self.pos_list.append(find_result)
                    #print("%s:%d" % (tag_label, find_result))
                    return find_result
                else:
                    start_pos = find_result + len(tag_label)
                    #print("already found one!")
        # if tag_label was not found,return -1
        #print("%s not found" % tag_label)
        return find_result

    def get_tag_lastpos(self, tag_name):
        pos = 0
        if self.tag_list == []:
            return pos
        i = len(self.tag_list)
        while i >= 1:
            tag_obj = self.tag_list[i - 1]
            if tag_obj.name== tag_name:
                pos = tag_obj.pos + len(tag_name)
                break
            i = i -1
        return pos
        
    def get_tag_allpair(self,tag_name):
    #find position of tag_name pair, return a list of pair pos
      tag_pair = '</'+tag_name+'>'
      start_pos = 0
      find_result = 0
      pair_pos = []
      while self.html.find(tag_pair,start_pos)!= -1:
      #keep seeking pair pos till it is not found
        find_result = self.html.find(tag_pair, start_pos)
        if find_result != -1:
            pair_pos.append(find_result)
            start_pos = find_result+len(tag_pair)
      return pair_pos
      
    def match_tag(self,tag_pos_list,pair_pos_list):
    # match the list of pos and pair, return a list of match. the biggest pos of pair, should match with biigest pos who is smaller than pair.
      match_list=[]
      #print('%s:\n%s'%(tag_pos_list,pair_pos_list))
      if tag_pos_list != []:
      #if tag_pos_list not empty,set min pos as first element of tag_post_list
        min_pos = tag_pos_list[0]
      else:
      #if tag_pos_list is empty, stop matching and return a empty match_list
        return match_list
      for pair_pos in pair_pos_list:
        for tag_pos in tag_pos_list:
          if (tag_pos<pair_pos) and (tag_pos>min_pos):
            min_pos = tag_pos
            #print(min_pos)
        match_list.append([min_pos,pair_pos])
        tag_pos_list.remove(min_pos)
          #remove min_pos from tag_pos_list as it has been matched
        if tag_pos_list !=[]:
        #if tag_pos_list not empty,set min pos as first element of tag_post_list
          min_pos = tag_pos_list[0]
        else:
          #if tag_pos_list is empty,stop matching
          return match_list
      return match_list
        
    def set_pair(self):
     #get pair position of tag
      #print(self.tag_list)
      for each in self.tag_list:
      #get each tag object in tag_list
          if each.tag_label[-2:]== '/>':
          #if tag end with />, directly get the pair position.
            each.pairpos = each.pos + len(each.tag_label)-2
            each.pair = '/>'
          #else if pair pos not exists, group the tags and get all tag position.
          elif each.pairpos ==-1:
            tag_pos_list=[]
            for ea in self.tag_list:
            #group tag pos for those tag_label == current tag label
              if ea.name ==each.name:
                tag_pos_list.append(ea.pos)
                #print(tag_pos_list)
            #get relevant pair pos list
            #print(tag_pos_list)
            tag_pair_list = self.get_tag_allpair(each.name)
            #match pair for tag,name of which ==current tag_label
            match_list = self.match_tag(tag_pos_list,tag_pair_list)
            #print(match_list)
            #update pair and pair pos by match list by go through each elements in math list.
            for ml in match_list:
              for tg in self.tag_list:
                if tg.pos == ml[0]:
                  tg.pairpos = ml[1]
                  tg.pair = '</'+tg.name+'>'
            
    def set_tag_content(self):
    #set tag content and children when tag pos and pair were set.
      for ea in self.tag_list:
        if ea.pairpos != -1:
        #when pair position is available, get tag content by str split
          ea.content = self.html[ea.pos:ea.pairpos + len(ea.pair)]
          content_str = ea.content
          content_str=content_str[len(ea.tag_label):]
          #if there is a string, it means the tag has children and indepent pair.
          if content_str != '':
            end = len(ea.name)+3
            content_str=content_str[:-end]
          ea.children = content_str

    def tag_set(self):
        # remove all tag setting, create tag object for all tags detected from txt.
        self.tag_list = []
        items = self.tag_items
        for ea in items:
            # define a tag object, and update tag of spider, id, description
            tag_object = tag_obj()
            # get the tag position in html
            start_pos = self.get_tag_lastpos(ea)
            pos = self.get_tag_pos(ea, start_pos)
            if pos != -1:
                tag_object.pos = pos
            else:
                tag_object.pos = 0
            tag_object.tag_label = ea
            # remove start and end of tag
            ea_str = ea
            tag_item = ea_str.replace(">", "")
            ea_str = tag_item.replace("<", "")
            # if there is a space, name is first part of string. otherwise, it is a none description tag, tag name equal to tag item.
            if ea_str.find(" "):
                ea_list = ea_str.split(" ")
                tag_object.name = ea_list[0]
            else:
                tag_object.name = ea_str
            # add tag_object into tag attribute
            # get class name of tag
            class_str = 'class="(.*?)"'
            pa_class = re.compile(class_str)
            class_content = re.findall(pa_class, ea)
            if class_content != []:
              tag_object.class_name = class_content[0]
            self.tag_list.append(tag_object)
        self.set_pair()
        self.set_tag_content()
        #when tag_list has been set up, match pos and pair pos.
    def get_tag_content(self,tag_name,class_name =''):
    #get tag content by input the tag name and class name(optional)
      tag_content =[]
      for ea in self.tag_list:
        if ea.name == tag_name:
          if class_name =="":
            tag_content.append(ea.content)
          elif ea.class_name == class_name:
            tag_content.append(ea.content)
      return tag_content
      
    def tag(self,tag_name,tag_classname =''):
    #get a tag_object by input the name, and there is more than 1 tag with same name, return first one. if tag was not exisiting, return a None
      tag_obj=None
      for tg in self.tag_list:
        if tg.name == tag_name:
          if tag_classname =='':
            tag_obj =tg
            break
          elif tag_classname in tg.class_name:
            tag_obj = tg
            break
      return tag_obj
          
      
   
         
            
       
            
          
          
        
