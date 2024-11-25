import sys
from collections import defaultdict
import xml.etree.ElementTree as ET
from xml.dom import minidom
class Command():
    def __init__(self):
        self.command=[]

    def add_to_com(self,com):
        self.command.append(f"0x{com}")
    def set_ABC(self,a,b,c):
        self.a=a
        self.b=b
        self.c=c

    def set_ABCDE(self, a, b, c,d,e):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e
    def get_command(self):
        res=""
        for i in self.command:
            res+=f"{i}, "
        return res[:-2]

    def xmlify(self):
        log_entry = ET.Element("command")
        ET.SubElement(log_entry, "A").text = str(self.a)
        ET.SubElement(log_entry, "B").text = str(self.b)
        ET.SubElement(log_entry, "C").text = str(self.c)
        if hasattr(self,"d"):
            ET.SubElement(log_entry, "D").text = str(self.d)
            ET.SubElement(log_entry, "E").text = str(self.e)
        ET.SubElement(log_entry, "command_bytes").text = str(self.get_command())

        return log_entry

def work(s):
    memory = defaultdict(lambda: 0)
    commands=[]
    for par in range(len(s)//8):
        com=""

        commands.append(Command())

        for cm in s[par*8:(par+1)*8]:

            com=format(int(cm,16),"08b")+com
            commands[-1].add_to_com(cm)

        oper=int(com[::-1][0:5+1][::-1],2)

        if oper==35:
            address=int(com[::-1][6:22+1][::-1],2)
            const=int(com[::-1][23:36+1][::-1],2)

            memory[address]=const
            commands[-1].set_ABC(35,address,const)
        elif oper==58:
            address_res=int(com[::-1][6:22+1][::-1],2)
            address=int(com[::-1][23:39+1][::-1],2)
            memory[address_res]=memory[memory[address]]
            commands[-1].set_ABC(58, address_res, address)
        elif oper==16:
            address_res=int(com[::-1][6:22+1][::-1],2)
            address=int(com[::-1][23:39+1][::-1],2)
            memory[memory[address_res]]=memory[address]
            commands[-1].set_ABC(16, address_res, address)
        elif oper==54:

            address_res = int(com[::-1][6:22 + 1][::-1], 2)
            address1 = int(com[::-1][23:39 + 1][::-1], 2)
            address2 = int(com[::-1][40:56 + 1][::-1], 2)
            offset= int(com[::-1][57:62 + 1][::-1], 2)
            memory[address_res]=int(memory[address1]==memory[address2+offset])
            commands[-1].set_ABCDE(54, address_res, address1,address2,offset)

    return memory,commands

if __name__ == "__main__":
    f = open("input_test.txt", "r")
    s = f.read().replace(",", "").replace(" ", "").replace("\n", "").split("0x")[1:]
    memory,commands=work(s)

#17 b 14

    log = ET.Element("log")
    coms=ET.SubElement(log,"commands")
    for i in commands:
        coms.append(i.xmlify())

    output=ET.Element("output")

    mem=ET.SubElement(log,"memory")
    mem_bin = ""
    for i in memory.keys():
        mem_bin+=format(i,"017b")+format(memory[i],"014b")

        ET.SubElement(mem,f"cell_{str(i)}").text=str(memory[i])

    ET.SubElement(output,"data").text=mem_bin
    raw_xml = ET.tostring(log, encoding="utf-8")

    pretty_xml = minidom.parseString(raw_xml).toprettyxml(indent="    ")

    ET.ElementTree(output).write("output.xml", encoding="utf-8", xml_declaration=True)
    open("log.xml","w").write(pretty_xml)
    print("Great succes Нраица")


