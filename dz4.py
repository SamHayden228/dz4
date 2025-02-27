import sys
from collections import defaultdict
import xml.etree.ElementTree as ET
from xml.dom import minidom
asse=""
def binary_to_hex(binary_str):
    # Убедимся, что длина кратна 4, добавляя нули слева
    binary_str = binary_str.zfill((len(binary_str) + 3) // 4 * 4)
    # Перевод в шестнадцатеричное
    hex_str = hex(int(binary_str, 2))[2:].upper()
    return hex_str
class Command():
    def __init__(self,s):
        res = binary_to_hex(s)

        while len(res) < 16:
            res = "0" + res

        co = []
        for i in range(0, len(res)):
            if i % 2 != 0:
                co.append((res[i - 1] + res[i]).upper())
        self.command = co[::-1]


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
            res += f"0x{i}, "
        return res;
    def get_string(self):
        res=""
        res+=f"<A>{str(self.a)}</A>"
        res += f"<B>{str(self.b)}</B>"
        res += f"<C>{str(self.c)}</C>"
        if hasattr(self,"d"):
            res += f"<D>{str(self.d)}</D>"
            res += f"<E>{str(self.e)}</E>"
        res += f"<com>{str(self.get_command())}</com>"
        return res



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
    for par in range(len(s)//64):
        com=s[par*64:(par+1)*64]

        commands.append(Command(s[par*64:(par+1)*64]))



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
        else:
            print("Я такой команды не знаю")

    return memory,commands

def assmb(s):
    asse=""
    s=s.replace(",", "").replace(" ", "").replace("\n", "").split("0x")[1:]
    for par in range(len(s) // 8):
        com=""
        for cm in s[par * 8:(par + 1) * 8]:
            com = format(int(cm, 16), "08b") + com

        asse+=com
    return asse
if __name__ == "__main__":
    f = open(sys.argv[1], "r")
    asse=assmb(f.read())
    output = ET.Element("output")
    ET.SubElement(output, "data").text = asse
    ET.ElementTree(output).write(sys.argv[2], encoding="utf-8", xml_declaration=True)

    parser = ET.XMLParser(encoding="utf-8")
    tree = ET.parse(sys.argv[2], parser=parser)
    root = tree.getroot()
    rt = str(root.findall("data")[0].text)

    memory,commands=work(rt)

#17 b 14

    

    log = ET.Element("log")
    coms=ET.SubElement(log,"commands")
    for i in commands:
        coms.append(i.xmlify())

    output=ET.Element("output")

    mem=ET.SubElement(log,"memory")
    
    for i in memory.keys():
        

        ET.SubElement(mem,f"cell_{str(i)}").text=str(memory[i])

    
    raw_xml = ET.tostring(log, encoding="utf-8")
    
    
    pretty_xml = minidom.parseString(raw_xml).toprettyxml(indent="    ")

    
    open(sys.argv[3],"w").write(pretty_xml)
    print("Great succes Нраица")


