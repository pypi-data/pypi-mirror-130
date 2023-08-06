from curses import initscr, echo, noecho, cbreak, nocbreak, endwin, curs_set, start_color
import curses

class Curse:
    def __init__(self,nocursor:bool=True,color:bool=True,autostart:bool=True,keypad:bool=True):
        self.color=color
        self.menu_indexes=[]
        self.menu_colors=[]
        self.menu_indx=0
        self.screen=None
        if autostart:
            self.start(nocursor=nocursor,k=keypad)

    def start(self,nocursor=True,k=True) -> None:
        self.screen=initscr()
        self.clear()
        if self.color is not None:
            start_color()
        curs_set(0 if nocursor else 1)
        noecho()
        cbreak()
        if k:
            self.screen.keypad(1)

    def clear(self) -> None:
        self.screen.clear()

    def erase(self) -> None:
        self.screen.erase()

    def getscr(self) -> tuple:
        return self.screen.getmaxyx()

    def process_string(self,s):
        s=s.replace(' ','')
        s=s.replace('1',' ')
        s=s.replace('2','.')
        s=s.replace('3','-')
        s=s.replace('4','|')
        s=s.replace('[','')
        s=s.replace(']','')
        return s

    def render_matrix(self,matrix:list=[[]]):
        for indx,itm in enumerate(matrix):
            for sindx, sitm in enumerate(itm):
                s=str(sitm)
                if len(s)>1:
                    color=int(s[1])
                    s=self.process_string(s[0])
                    self.display(sindx,indx,text=s,color_pair=color)
                else:
                    self.display(sindx,indx,self.process_string(s[0]))

    def add_color_pair(self,pair_id:int,fore:str='blue',back:str='red') -> int:
        if not self.color:
            return 
        string="".join(['curses.init_pair(',str(pair_id),',curses.COLOR_{},curses.COLOR_{})'.format(fore.upper(),back.upper())])
        eval(string)
        return pair_id

    def menu_board(self,options:list=['Hello','World'],color_pairs:list=None,add_to_memory:bool=True):
        self.clear()
        h,w=self.getscr()
        if add_to_memory:
            self.menu_indexes=options
            self.menu_colors=color_pairs
        for indx,row in enumerate(options):
            x=w//2-len(row)//2
            y=h//2-len(options)//2+indx
            if color_pairs[indx] is not None:
                self.display(x,y,row,color_pair=color_pairs[indx])
                continue 
            self.display(x,y,row)

    def menu_board_input(self,cursor:str='5|$field <',inputs:list=["display_mid('Pressed')"]):
        cursor=cursor.split(sep='|')
        rep=cursor[1]
        color=int(cursor[0])

        while 1:   
            key=self.screen.getch()

            self.clear()
            indexes=list(self.menu_indexes)
            colors=list(self.menu_colors)

            if key==curses.KEY_UP and self.menu_indx>0:
                self.menu_indx-=1

            elif key==curses.KEY_DOWN and self.menu_indx<len(self.menu_indexes)-1:
                self.menu_indx+=1

            elif key==curses.KEY_ENTER or key in [10,13]:
                r=inputs[self.menu_indx].replace('$.','self.')
                if r != 'break':
                    eval(r)
                else:
                    break

            indexes[self.menu_indx]=rep.replace('$field',indexes[self.menu_indx])
            colors[self.menu_indx]=color

            self.menu_board(indexes,colors,add_to_memory=False)

            self.refresh()
      
        return self.menu_indexes[self.menu_indx]

    def setkey(self,val:bool=True):
        self.screen.keypad(val)

    def display_mid(self,text:str='Hello World',color_pair:int=None) -> None:
        h,w=self.screen.getmaxyx()
        x=w//2 - len(text)//2
        y=h//2
        if color_pair is not None:
            self.screen.attron(curses.color_pair(color_pair))
            self.screen.addstr(y,x,text)
            self.screen.attroff(curses.color_pair(color_pair))
        else:
            self.screen.addstr(y,x,text)

    def display(self,x,y,text:str='Hello World',color_pair:int=None) -> None:
        if color_pair is not None:
            self.screen.attron(curses.color_pair(color_pair))
            self.screen.addstr(y,x,text)
            self.screen.attroff(curses.color_pair(color_pair))
        else:
            self.screen.addstr(y,x,text)

    def refresh(self) -> None:
        self.screen.refresh()

    def close(self) -> None:
        curs_set(1)
        echo()
        nocbreak()
        endwin()