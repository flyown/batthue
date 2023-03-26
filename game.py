from abc import abstractmethod
import glob
import pygame
import sys
import cv2 as cv
import numpy as np

SCREEN_W=640
SCREEN_H=480
SCREEN=pygame.Rect(0,0,SCREEN_W,SCREEN_H) # 4:3
yellow_low=np.array([15,32,32])
yellow_high=np.array([44,255,255])
green_low=np.array([45,32,32])
green_high=np.array([74,255,255])
cian_low=np.array([75,32,32])
cian_high=np.array([104,255,255])
blue_low=np.array([105,32,32])
blue_high=np.array([134,255,255])
magenta_low=np.array([135,32,32])
magenta_high=np.array([164,255,255])
red_low=np.array([165,32,32])
red_high=np.array([180,255,255])
red_low2=np.array([0,32,32])
red_high2=np.array([14,255,255])
black_low=np.array([0,0,0])
black_high=np.array([180,31,127])
white_low=np.array([0,0,128])
white_high=np.array([180,31,255])

color=[[0,yellow_low,yellow_high],[1,green_low,green_high],[2,cian_low,cian_high],[3,blue_low,blue_high],[4,magenta_low,magenta_high],[5,[red_low,red_low2],[red_high,red_high2]],[6,black_low,black_high],[7,white_low,white_high]]
what_is_color=[(255,255,0),(0,255,0),(0,255,255),(0,0,255),(255,0,255),(255,0,0),(0,0,0),(255,255,255)]


pygame.init()
screen=pygame.display.set_mode(SCREEN.size)
pygame.display.set_caption("batthue")
japanes=pygame.font.Font("fonts/ipaexm.ttf",30)
bigjapanese=pygame.font.Font("fonts/ipaexm.ttf",50)
clock = pygame.time.Clock()

# メッセージウィンドウ
class Message_Window(pygame.sprite.Sprite):
    def __init__(self):
        #pygame.sprite.Sprite.__init__(self,self.containers)
        self.rect=pygame.Rect(2,SCREEN_H-140,SCREEN_W-4,136)

    def draw(self):
        pygame.draw.rect(screen,(0,0,0),self.rect,4)

    def weapon_draw(self,weapon):#わざの表示
        x=70
        y=SCREEN_H-110
        for i in range(len(weapon)):
            if i==2:
                x=70
                y=SCREEN_H-60
            txt=japanes.render("わざ{}".format(i+1),True,(0,0,0))
            screen.blit(txt,(x,y))
            x+=170
        x=410
        y=SCREEN_H-60
        txt=japanes.render("あいしょう",True,(0,0,0))
        screen.blit(txt,(x,y))
        mouse_pos=pygame.mouse.get_pos()
        mx=mouse_pos[0]
        my=mouse_pos[1]
        if mx>60 and mx<200:
            if my>SCREEN_H-120 and my<SCREEN_H-70:
                pygame.draw.polygon(screen,(0,0,0),[[65,SCREEN_H-95],[55,SCREEN_H-105],[55,SCREEN_H-85]])
                self.weapon_detail(weapon,0)
            elif my>SCREEN_H-70 and my<SCREEN_H-20 and len(weapon)>=3:
                pygame.draw.polygon(screen,(0,0,0),[[65,SCREEN_H-45],[55,SCREEN_H-55],[55,SCREEN_H-35]])
                self.weapon_detail(weapon,2)
        elif mx>230 and mx<370:
            if my>SCREEN_H-120 and my<SCREEN_H-70 and len(weapon)>=2:
                pygame.draw.polygon(screen,(0,0,0),[[235,SCREEN_H-95],[225,SCREEN_H-105],[225,SCREEN_H-85]])
                self.weapon_detail(weapon,1)
            elif my>SCREEN_H-70 and my<SCREEN_H-20 and len(weapon)>=4:
                pygame.draw.polygon(screen,(0,0,0),[[235,SCREEN_H-45],[225,SCREEN_H-55],[225,SCREEN_H-35]])
                self.weapon_detail(weapon,3)
        elif mx>400 and mx<540 and my>SCREEN_H-70 and my<SCREEN_H-20:
            pygame.draw.polygon(screen,(0,0,0),[[405,SCREEN_H-45],[395,SCREEN_H-55],[395,SCREEN_H-35]])
            self.compatibility()

    def weapon_detail(self,weapon,choice):#わざの詳細表示
        pygame.draw.rect(screen,(255,255,255),(400,250,200,170),0)
        pygame.draw.rect(screen,(0,0,0),(400,250,200,170),4)
        w_type=japanes.render("タイプ :",True,(0,0,0))
        if weapon[choice][0]>=6:
            w_iryoku=japanes.render("種類 :",True,(0,0,0))
            x=430
        else:
            w_iryoku=japanes.render("威力 :",True,(0,0,0))
            w_iryoku2=japanes.render("{}".format(weapon[choice][1]),True,(0,0,0))
            x=500
        screen.blit(w_type,(410,260))
        if weapon[choice][0]==7:
            txt=japanes.render("強化",True,(0,0,0))
            screen.blit(txt,(450,300))
            s="+"*weapon[choice][2]
            w_iryoku2=japanes.render(weapon[choice][1]+s,True,(0,0,0))
        elif weapon[choice][0]==6:
            txt=japanes.render("弱体化",True,(0,0,0))
            screen.blit(txt,(450,300))
            s="-"*weapon[choice][2]
            w_iryoku2=japanes.render(weapon[choice][1]+s,True,(0,0,0))
        else:
            pygame.draw.rect(screen,what_is_color[weapon[choice][0]],(430,300,140,30),0)
        screen.blit(w_iryoku,(410,340))
        screen.blit(w_iryoku2,(x,380))

    def compatibility(self):#相性の表示
        compati=pygame.image.load("system/compatibility.png")
        compati=pygame.transform.scale(compati,(400,400))
        screen.blit(compati,(120,10))

    def attack(self,attacker):#攻撃時のメッセージ
        txt=japanes.render("{}のこうげき！".format(attacker.name),True,(0,0,0))
        screen.blit(txt,(60,SCREEN_H-110))

    def lose(self,loser):#倒した・倒されたとき
        txt=japanes.render("{}はたおれた！".format(loser.name),True,(0,0,0))
        screen.blit(txt,(60,SCREEN_H-110))

    def clear(self):#クリアした時
        txt=japanes.render("クリア！",True,(0,0,0))
        screen.blit(txt,(60,SCREEN_H-110))

    def gameover(self):#ゲームオーバー時
        txt=japanes.render("ゲームオーバー…",True,(0,0,0))
        screen.blit(txt,(60,SCREEN_H-110))

    def batsugun(self):#効果抜群のわざを使った時
        txt=japanes.render("こうかは　ばつぐんだ！",True,(0,0,0))
        screen.blit(txt,(60,SCREEN_H-70))
    
    def cure(self,name):#回復した時
        txt=japanes.render("{}は回復した！".format(name),True,(0,0,0))
        screen.blit(txt,(60,SCREEN_H-110))

    def w_add(self):#わざ追加時
        txt=japanes.render("わざを追加した！",True,(0,0,0))
        screen.blit(txt,(60,SCREEN_H-110))

    def w_change(self,num):#わざ変更時
        txt=japanes.render("わざ{}を変更した！".format(num+1),True,(0,0,0))
        screen.blit(txt,(60,SCREEN_H-110))

    def buff(self,target,weapon):#バフしたとき
        txt=japanes.render("{}は強化技を繰り出した！".format(target.name),True,(0,0,0))
        screen.blit(txt,(60,SCREEN_H-110))
        if weapon[2]==2:
            s="ぐーんと"
        else:
            s=""
        txt=japanes.render("{}の{}が".format(target.name,weapon[1])+s+"あがった！",True,(0,0,0))
        screen.blit(txt,(60,SCREEN_H-70))

    def debuff(self,me,target,weapon):#デバフしたとき
        txt=japanes.render("{}は弱体化技を繰り出した！".format(me.name),True,(0,0,0))
        screen.blit(txt,(60,SCREEN_H-110))
        if weapon[2]==2:
            s="がくっと"
        else:
            s=""
        txt=japanes.render("{}の{}が".format(target.name,weapon[1])+s+"さがった！",True,(0,0,0))
        screen.blit(txt,(60,SCREEN_H-70))

    def show_status(self,target):#ステータス表示
        hp=int(target.health)
        nowHP=int(target.HP.get_nowhp())
        attack=int(target.attack)
        speed=int(target.speed)
        defence=int(target.defence)
        hp_txt=japanes.render("HP : {}/{}".format(nowHP,hp),True,(0,0,0))
        attack_txt=japanes.render("こうげき : {}".format(attack),True,(0,0,0))
        speed_txt=japanes.render("すばやさ : {}".format(speed),True,(0,0,0))
        defence_txt=japanes.render("ぼうぎょ : {}".format(defence),True,(0,0,0))
        screen.blit(hp_txt,(70,SCREEN_H-110))
        screen.blit(attack_txt,(340,SCREEN_H-110))
        screen.blit(defence_txt,(70,SCREEN_H-60))
        screen.blit(speed_txt,(340,SCREEN_H-60))

    def toutatu(self,level):#ゲームオーバー時にn層まで到達したことを示す
        txt=japanes.render("{}層まで到達".format(level),True,(0,0,0))
        screen.blit(txt,(60,SCREEN_H-70))
            
# HPバー
class HP_bar(pygame.sprite.Sprite):
    def __init__(self,x,y,maxhealth):
        #pygame.sprite.Sprite.__init__(self,self.containers)
        self.x=x
        self.y=y
        self.rect=pygame.Rect(self.x,self.y,200,40)
        self.nowHP=maxhealth

    def draw(self,health):
        if self.nowHP/health>0.5:
            color=(100,255,100)
        elif self.nowHP/health>0.2:
            color=(255,255,0)
        else:
            color=(255,0,0)
        pygame.draw.rect(screen,color,(self.x,self.y,200*self.nowHP/health,40),0)
        pygame.draw.rect(screen,(0,0,0),self.rect,2)

    def hp_update(self,damage):#HPの更新
        self.nowHP-=damage

    def get_nowhp(self):#現在HPの確認
        return self.nowHP

# 自分と敵の共通部
class Character(pygame.sprite.Sprite):
    def __init__(self,x,y,r,color,HP):
        #pygame.sprite.Sprite.__init__(self,self.containers)
        self.x=x
        self.y=y
        self.r=r
        self.color=color
        self.HP=HP
        self.buff=[0,0,0]
        self.debuff=[0,0,0]

    def draw(self):
        pygame.draw.circle(screen,self.color,(self.x,self.y),self.r,0)
        pygame.draw.circle(screen,(0,0,0),(self.x,self.y),self.r,4)
        self.HP.draw(self.health)

    @abstractmethod
    def set_status(self):
        pass

    def receive_damage(self,weapon,opponent):#受けるダメージ計算
        damage=0
        batsugun_flag=False
        buff_flag=False
        debuff_flag=False
        if weapon[0]<6:
            damage=int(weapon[1]*((opponent.attack*(1+opponent.buff[0]/2)*(2/(opponent.debuff[0]+2)))/(self.defence*(1+self.buff[1]/2)*(2/(2+self.debuff[1]))))*1/25)
            if not (self.color[0]==what_is_color[weapon[0]][0] or self.color[1]==what_is_color[weapon[0]][1] or self.color[2]==what_is_color[weapon[0]][2]):
                damage=2*damage
                batsugun_flag=True
        elif weapon[0]==7:
            opponent.set_buff(weapon)
            buff_flag=True
        elif weapon[0]==6:
            self.set_debuff(weapon)
            debuff_flag=True
        return damage,batsugun_flag,buff_flag,debuff_flag

    def check_death(self):#倒れたか
        nowHP=self.HP.get_nowhp()
        if nowHP<=0:
            return True
        else:
            return False

    def set_buff(self,weapon):#バフ追加
        buff=weapon[1]
        if buff=="こうげき":
            if self.debuff[0]>0:#デバフがあったら打ち消し
                self.debuff[0]-=weapon[2]
                i=0
                if self.debuff[0]<0:
                    i=-self.debuff[0]
                    self.debuff[0]=0
                self.buff[0]+=i
            else:
                self.buff[0]+=weapon[2]
        elif buff=="ぼうぎょ":
            if self.debuff[1]>0:
                self.debuff[1]-=weapon[2]
                i=0
                if self.debuff[1]<0:
                    i=-self.debuff[1]
                    self.debuff[1]=0
                self.buff[1]+=i
            else:
                self.buff[1]+=weapon[2]
        elif buff=="すばやさ":
            if self.debuff[2]>0:
                self.debuff[2]-=weapon[2]
                i=0
                if self.debuff[2]<0:
                    i=-self.debuff[2]
                    self.debuff[2]=0
                self.buff[2]+=i
            else:
                self.buff[0]+=weapon[2]

    def set_debuff(self,weapon):#デバフ追加
        debuff=weapon[1]
        if debuff=="こうげき":
            if self.buff[0]>0:#バフがあったら打ち消し
                self.buff[0]-=weapon[2]
                i=0
                if self.buff[0]<0:
                    i=-self.buff[0]
                    self.buff[0]=0
                self.debuff[0]+=i
            else:
                self.debuff[0]+=weapon[2]
        elif debuff=="ぼうぎょ":
            if self.buff[1]>0:
                self.buff[1]-=weapon[2]
                i=0
                if self.buff[1]<0:
                    i=-self.buff[1]
                    self.buff[1]=0
                self.debuff[1]+=i
            else:
                self.debuff[1]+=weapon[2]
        elif debuff=="すばやさ":
            if self.buff[2]>0:
                self.buff[2]-=weapon[2]
                i=0
                if self.buff[2]<0:
                    i=-self.buff[2]
                    self.buff[2]=0
                self.debuff[2]+=i
            else:
                self.debuff[2]+=weapon[2]

# 自分
class My_Chara(Character):
    def __init__(self,color,image):
        self.name="自分"
        self.use_image_color=image
        self.weapon=[]
        self.set_weapon()
        self.set_status()
        self.HP=HP_bar(400,200,self.health)
        super().__init__(150,250,70,color,self.HP)

    def set_weapon(self):#初期わざ決定
        sorted_color=sorted(self.use_image_color,reverse=True)
        for i,sc in enumerate(sorted_color):
            if sc <0.05:#面積が小さすぎる場合は無視
                break
            for col,ar in enumerate(self.use_image_color):#面積が同じ場合にわざが重複しないように
                flag=False
                if sc==ar:
                    if i==0:
                        break
                    else:
                        for w in self.weapon:
                            if col==w[0]:
                                flag=True
                        if flag:
                            continue
                        else:
                            break
            if col>=6:#バフデバフ（白黒）の場合
                if what_is_color[self.weapon[0][0]][0]==255:
                    r=1
                else:
                    r=0
                if what_is_color[self.weapon[0][0]][1]==255:
                    g=1
                else:
                    g=0
                if what_is_color[self.weapon[0][0]][2]==255:
                    b=1
                else:
                    b=0
                effect=[]
                if r:
                    effect.append("こうげき")
                if g:
                    effect.append("ぼうぎょ")
                if b:
                    effect.append("すばやさ")
                s=np.random.choice(effect)
                iryoku=int(50+5*sc//0.05)
                if iryoku>100:
                    j=2
                else:
                    j=1
                self.weapon.append([col,s,j])
            else:
                self.weapon.append([col,int(50+5*sc//0.05)])
            if i>=3:
                break
    
    def set_status(self):#初期ステータス
        self.health=100+10*self.use_image_color[1]//0.05+5*self.use_image_color[0]//0.1+5*self.use_image_color[2]//0.1
        self.attack=10+3*self.use_image_color[5]//0.05+self.use_image_color[0]//0.1+self.use_image_color[4]//0.1
        self.speed=10+3*self.use_image_color[3]//0.05+self.use_image_color[4]//0.1+self.use_image_color[2]//0.1
        self.defence=10+self.use_image_color[1]//0.1+self.use_image_color[3]//0.1+self.use_image_color[5]//0.1+self.use_image_color[0]//0.2+self.use_image_color[2]//0.2+self.use_image_color[4]//0.2

    def status_up(self,up):#ステータス増加
        if up[0]=="HP":
            self.health+=up[1]
            self.HP.hp_update(-up[1])
        elif up[0]=="こうげき":
            self.attack+=up[1]
        elif up[0]=="ぼうぎょ":
            self.defence+=up[1]
        else:
            self.speed+=up[1]

    def cure(self,num):#回復
        nowHP=self.HP.get_nowhp()
        hp=min(nowHP+num,self.health)
        self.HP.hp_update(nowHP-hp)

# 敵
class Enemy(Character):
    def __init__(self,color,image,num):
        self.name="敵"
        self.use_image_color=image
        self.weapon=[]
        self.set_status(num)
        self.HP=HP_bar(60,60,self.health)
        super().__init__(490,110,40,color,self.HP)
        self.set_weapon(num)
        self.num=num

    def set_weapon(self,num):#初期わざ
        sorted_color=sorted(self.use_image_color,reverse=True)
        for i,sc in enumerate(sorted_color):
            if sc <0.05:
                break
            col=self.use_image_color.index(sc)
            if col>=6:
                if what_is_color[self.weapon[0][0]][0]==255:
                    r=1
                else:
                    r=0
                if what_is_color[self.weapon[0][0]][1]==255:
                    g=1
                else:
                    g=0
                if what_is_color[self.weapon[0][0]][2]==255:
                    b=1
                else:
                    b=0
                effect=[]
                if r:
                    effect.append("こうげき")
                if g:
                    effect.append("ぼうぎょ")
                if b:
                    effect.append("すばやさ")
                s=np.random.choice(effect)
                iryoku=int(min(50,num//4*10+30)+5*sc//0.05)
                if iryoku>100:
                    j=2
                else:
                    j=1
                self.weapon.append([col,s,j])
            else:
                self.weapon.append([col,int(min(50,num//4*10+30)+5*sc//0.05)])
            if i>=3 or i>=num//4:
                break

    def set_status(self,num):#初期ステータス
        self.health=10*num+50+5*self.use_image_color[1]//0.05+self.use_image_color[0]//0.1+self.use_image_color[2]//0.1
        self.attack=2*num+5+3*self.use_image_color[5]//0.05+self.use_image_color[0]//0.1+self.use_image_color[4]//0.1
        self.speed=2*num+5+3*self.use_image_color[3]//0.05+self.use_image_color[4]//0.1+self.use_image_color[2]//0.1
        self.defence=num+5+self.use_image_color[1]//0.1+self.use_image_color[3]//0.1+self.use_image_color[5]//0.1+self.use_image_color[0]//0.2+self.use_image_color[2]//0.2+self.use_image_color[4]//0.2

    def name_draw(self):
        txt=japanes.render("{} (level {})".format(self.name,self.num),True,(0,0,0))
        screen.blit(txt,(60,25))

#ボス
class BOSS(Character):
    def __init__(self,num):
        color,self.use_image_color,name=self.color_read()
        self.name=name.split(".")[0]
        self.weapon=[]
        self.set_status(num)
        self.HP=HP_bar(60,60,self.health)
        super().__init__(490,110,40,color,self.HP)
        self.set_weapon()

    def color_read(self):#画像フォルダからランダムで使用する画像を選択して生成
        files=glob.glob("./image/*")
        file=np.random.choice(files)
        img=cv.imread(file)
        h,w,_=img.shape
        size=h*w
        Area_rs=[]
        hsv_img=cv.cvtColor(img,cv.COLOR_BGR2HSV)
        for i,low,high in color:
            if len(low)==2:
                mask1=cv.inRange(hsv_img,low[0],high[0])
                mask2=cv.inRange(hsv_img,low[1],high[1])
                mask=mask1+mask2
            else:
                mask=cv.inRange(hsv_img,low,high)
            color_area=cv.countNonZero(mask)
            area_r=color_area/size
            if i>6:
                rnd=np.random.randint(0,6)
                Area_rs[rnd]+=area_r
                Area_rs.append(area_r)
            else:
                Area_rs.append(area_r)
        if Area_rs.count(max(Area_rs))>1:
            ind=[]
            for i,ar in enumerate(Area_rs):
                if i>=6:
                    continue
                if ar==max(Area_rs):
                    ind.append(i)
            max_color_num=np.random.choice(ind)
        else:
            max_color_num=Area_rs.index(max(Area_rs))
        return what_is_color[max_color_num],Area_rs,file.split("/")[-1]

    def set_status(self,num):
        self.health=(num//10)*60+100+10*self.use_image_color[1]//0.05+5*self.use_image_color[0]//0.1+5*self.use_image_color[2]//0.1
        self.attack=(num//10)*6+10+3*self.use_image_color[5]//0.05+self.use_image_color[0]//0.1+self.use_image_color[4]//0.1
        self.speed=(num//10)*6+10+3*self.use_image_color[3]//0.05+self.use_image_color[4]//0.1+self.use_image_color[2]//0.1
        self.defence=(num//10)*6+10+self.use_image_color[1]//0.1+self.use_image_color[3]//0.1+self.use_image_color[5]//0.1+self.use_image_color[0]//0.2+self.use_image_color[2]//0.2+self.use_image_color[4]//0.2
        
    def set_weapon(self):
        sorted_color=sorted(self.use_image_color,reverse=True)
        for i,sc in enumerate(sorted_color):
            if sc <0.05:
                break
            col=self.use_image_color.index(sc)
            if col>=6:
                if what_is_color[self.weapon[0][0]][0]==255:
                    r=1
                else:
                    r=0
                if what_is_color[self.weapon[0][0]][1]==255:
                    g=1
                else:
                    g=0
                if what_is_color[self.weapon[0][0]][2]==255:
                    b=1
                else:
                    b=0
                effect=[]
                if r:
                    effect.append("こうげき")
                if g:
                    effect.append("ぼうぎょ")
                if b:
                    effect.append("すばやさ")
                s=np.random.choice(effect)
                iryoku=int(50+5*sc//0.05)
                if iryoku>100:
                    j=2
                else:
                    j=1
                self.weapon.append([col,s,j])
            else:
                self.weapon.append([col,int(50+5*sc//0.05)])
            if i>=3:
                break

    def name_draw(self):
        txt=japanes.render("{}".format(self.name),True,(0,0,0))
        screen.blit(txt,(60,25))

# 画像取得・選択画面
def get_image_file(files):
    next_status=2
    finflag=False
    img=None
    screen.fill((255,255,255))
    txt=japanes.render("画像を選択",True,(0,0,0))
    screen.blit(txt,(SCREEN_W/3+20,20))
    h=70
    for file in files:
        file=file.split("/")
        txt=japanes.render(file[-1],True,(0,0,0))
        screen.blit(txt,(SCREEN_W/4+30,h))
        h+=35
    mouse_pos=pygame.mouse.get_pos()
    choice=mouse_pos[1]//35-2
    if choice>=0 and choice<len(files):
        pygame.draw.rect(screen,(255,0,0),(SCREEN_W/4+28,70+35*choice,250,32),2)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
            if choice>=0 and choice<len(files):
                imstr=files[choice]
                img=cv.imread("{}".format(imstr))
                finflag=True
                next_status=3
        if event.type == pygame.QUIT:
                next_status=-1
    return next_status,finflag,img

# 画像読み込み
def color_read(img):
    h,w,_=img.shape
    size=h*w
    Area_rs=[]
    hsv_img=cv.cvtColor(img,cv.COLOR_BGR2HSV)
    for i,low,high in color:
        if len(low)==2:
            mask1=cv.inRange(hsv_img,low[0],high[0])
            mask2=cv.inRange(hsv_img,low[1],high[1])
            mask=mask1+mask2
        else:
            mask=cv.inRange(hsv_img,low,high)
        color_area=cv.countNonZero(mask)
        area_r=color_area/size
        if i>=6:#白黒がメインカラーにならないように，白黒の面積を他の色(ランダム)の面積に加算
            rnd=np.random.randint(0,6)
            Area_rs[rnd]+=area_r
            Area_rs.append(area_r)
        else:
            Area_rs.append(area_r)
    if Area_rs.count(max(Area_rs))>1:#最大面積の色が複数ある場合，白黒でなければランダムでメインカラーに
        ind=[]
        for i,ar in enumerate(Area_rs):
            if i>=6:
                continue
            if ar==max(Area_rs):
                ind.append(i)
        max_color_num=np.random.choice(ind)
    else:
        max_color_num=Area_rs.index(max(Area_rs))
    return My_Chara(what_is_color[max_color_num],Area_rs)

# バトル内わざ選択画面
def battle_phase_choice(me,enemy,message_w):
    next_status=4
    attack=-1
    screen.fill((255,255,255))
    me.draw()
    enemy.draw()
    enemy.name_draw()
    message_w.draw()
    message_w.weapon_draw(me.weapon)
    pygame.display.update()

    for event in pygame.event.get():
        if event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
            mouse_pos=pygame.mouse.get_pos()
            mx=mouse_pos[0]
            my=mouse_pos[1]
            if mx>60 and mx<200:
                if my>SCREEN_H-120 and my<SCREEN_H-70:
                    attack=0
                    next_status=5
                elif my>SCREEN_H-70 and my<SCREEN_H-20 and len(me.weapon)>=3:
                    attack=2
                    next_status=5
            elif mx>230 and mx<370:
                if my>SCREEN_H-120 and my<SCREEN_H-70 and len(me.weapon)>=2:
                    attack=1
                    next_status=5
                elif my>SCREEN_H-70 and my<SCREEN_H-20 and len(me.weapon)>=4:
                    attack=3
                    next_status=5
                
            if event.type == pygame.QUIT:
                next_status=-1
    return next_status,attack

#バトル処理   
def battle_process(target,now_act,damage,batsugun,buff,debuff,me,enemy,message_w,weapon):
    finish=False
    if buff:
        pass
    elif debuff:
        pass
    elif damage>0:
        target.HP.hp_update(1)
        damage-=1
        if damage<=0:
            finish=True
    screen.fill((255,255,255))
    me.draw()
    enemy.draw()
    enemy.name_draw()
    message_w.draw()
    if buff:
        message_w.buff(now_act,weapon)
    elif debuff:
        message_w.debuff(now_act,target,weapon)
    else:
        message_w.attack(now_act)
        if batsugun:
            message_w.batsugun()
    pygame.display.update()
    if buff or debuff:
        finish=True
    return damage,finish

# レベルアップ画面
def level_up(me,status_up):
    next_status=7
    x=-1
    msg=Message_Window()
    screen.fill((255,255,255))
    msg.draw()
    msg.show_status(me)
    for i in range(3):
        pygame.draw.rect(screen,(0,0,0),(80+180*i,120,150,150),4)
        txt=japanes.render(status_up[i][0],True,(0,0,0))
        if status_up[i][0]=="HP":
            screen.blit(txt,(130+180*i,130))
        else:
            screen.blit(txt,(95+180*i,130))
        txt=japanes.render("+"+str(status_up[i][1]),True,(0,0,0))
        screen.blit(txt,(130+180*i,170))
    mouse_pos=pygame.mouse.get_pos()
    mx,my=mouse_pos[0],mouse_pos[1]
    if my>120 and my<270:
        if mx>80 and mx<230:
            pygame.draw.rect(screen,(255,255,0),(80,120,150,150),4)
        elif mx>260 and mx<410:
            pygame.draw.rect(screen,(255,255,0),(260,120,150,150),4)
        elif mx>440 and mx<590:
            pygame.draw.rect(screen,(255,255,0),(440,120,150,150),4)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
            if my>120 and my<270:
                if mx>80 and mx<230:
                    x=0
                    next_status=3
                elif mx>260 and mx<410:
                    x=1
                    next_status=3
                elif mx>440 and mx<590:
                    x=2
                    next_status=3

        if event.type==pygame.QUIT:
            next_status=-1
    return next_status,x

#回復か技の追加変更かを選ぶ画面  
def choice(me):
    next_status=8
    screen.fill((255,255,255))
    pygame.draw.rect(screen,(0,0,0),(150,120,150,150),4)
    pygame.draw.rect(screen,(0,0,0),(340,120,150,150),4)
    cure=japanes.render("回復",True,(0,0,0))
    w_add=japanes.render("技追加",True,(0,0,0))
    w_change=japanes.render("変更",True,(0,0,0))
    screen.blit(cure,(195,170))
    screen.blit(w_add,(380,140))
    screen.blit(w_change,(390,175))
    mx,my=pygame.mouse.get_pos()
    if mx>140 and mx<310 and my>110 and my<280:
        pygame.draw.rect(screen,(255,255,0),(150,120,150,150),4)
    elif mx>330 and mx<500 and my>110 and my<280:
        pygame.draw.rect(screen,(255,255,0),(340,120,150,150),4)
    pygame.display.update()

    for event in pygame.event.get():
        if event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
            if mx>140 and mx<310 and my>110 and my<280:
                next_status=9
            elif mx>330 and mx<500 and my>110 and my<280:
                next_status=10
        if event.type==pygame.QUIT:
            next_status=-1
    return next_status

#クリックしないと進まない処理
def click():
    endflag=True
    pygame.draw.polygon(screen,(0,0,0),[[SCREEN_W-25,SCREEN_H-25],[SCREEN_W-10,SCREEN_H-25],[SCREEN_W-17,SCREEN_H-13]])
    pygame.display.update()
    while endflag:
        for event in pygame.event.get():
            if event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
                endflag=False

            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()

#技変更するときに現在の技の中から何を忘れるか
def weaponchange_choice(me,msg):
    next_status=10
    finish=False
    change=-1
    screen.fill((255,255,255))
    txt=japanes.render("どの技を忘れる？",True,(0,0,0))
    screen.blit(txt,(185,120))
    msg.draw()
    msg.weapon_draw(me.weapon)
    pygame.display.update()

    for event in pygame.event.get():
        if event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
            mouse_pos=pygame.mouse.get_pos()
            mx=mouse_pos[0]
            my=mouse_pos[1]
            if mx>60 and mx<200:
                if my>SCREEN_H-120 and my<SCREEN_H-70:
                    change=0
                    finish=True
                elif my>SCREEN_H-70 and my<SCREEN_H-20 and len(me.weapon)>=3:
                    change=2
                    finish=True
            elif mx>230 and mx<370:
                if my>SCREEN_H-120 and my<SCREEN_H-70 and len(me.weapon)>=2:
                    change=1
                    finish=True
                elif my>SCREEN_H-70 and my<SCREEN_H-20 and len(me.weapon)>=4:
                    change=3
                    finish=True
        if event.type == pygame.QUIT:
            next_status=-1
    return next_status,finish,change

#技変更する時に選んだ画像のどの技を覚えるか
def weaponchange(msg,chara):
    next_status=10
    choice=-1
    screen.fill((255,255,255))
    txt=japanes.render("どの技を覚える？",True,(0,0,0))
    screen.blit(txt,(185,120))
    msg.draw()
    msg.weapon_draw(chara.weapon)
    pygame.display.update()

    for event in pygame.event.get():
        if event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
            mouse_pos=pygame.mouse.get_pos()
            mx=mouse_pos[0]
            my=mouse_pos[1]
            if mx>60 and mx<200:
                if my>SCREEN_H-120 and my<SCREEN_H-70:
                    choice=0
                    next_status=3
                elif my>SCREEN_H-70 and my<SCREEN_H-20 and len(chara.weapon)>=3:
                    choice=2
                    next_status=3
            elif mx>230 and mx<370:
                if my>SCREEN_H-120 and my<SCREEN_H-70 and len(chara.weapon)>=2:
                    choice=1
                    next_status=3
                elif my>SCREEN_H-70 and my<SCREEN_H-20 and len(chara.weapon)>=4:
                    choice=3
                    next_status=3
                
        if event.type == pygame.QUIT:
            next_status=-1
    return next_status,choice

#メニュー(タイトル)画面
def menu(title):
    next_status=0
    screen.fill((255,255,255))
    start=japanes.render("はじめる",True,(0,0,0))
    quit=japanes.render("おわる",True,(0,0,0))
    mx,my=pygame.mouse.get_pos()
    if mx>SCREEN_W/3+35 and mx<SCREEN_W/3+175:
        if my>SCREEN_H/4*2-10 and my<SCREEN_H/4*2+40:
            start=japanes.render("はじめる",True,(200,100,0))
        elif my>SCREEN_H/4*2+50 and my<SCREEN_H/4*2+100:
            quit=japanes.render("おわる",True,(200,100,0))
    screen.blit(start,(SCREEN_W/3+45,SCREEN_H/4*2))
    screen.blit(quit,(SCREEN_W/3+60,SCREEN_H/4*2+60))
    screen.blit(title,(-20,40))
    pygame.display.update()

    for event in pygame.event.get():
        if event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
            if mx>SCREEN_W/3+35 and mx<SCREEN_W/3+175:
                if my>SCREEN_H/4*2-10 and my<SCREEN_H/4*2+40:
                    next_status=1
                elif my>SCREEN_H/4*2+50 and my<SCREEN_H/4*2+100:
                    next_status=-1
        if event.type==pygame.QUIT:
            next_status=-1
    return next_status

#難易度選択画面
def difficulty():
    next_status=1
    screen.fill((255,255,255))
    level=["デモ用(5戦)","イージー(10戦)","ノーマル(20戦)","ハード(50戦)","エンドレス"]
    txt=japanes.render("難易度を選択",True,(0,0,0))
    screen.blit(txt,(SCREEN_W/3+20,20))
    h=70
    for l in level:
        txt=japanes.render(l,True,(0,0,0))
        screen.blit(txt,(SCREEN_W/4+30,h))
        h+=35
    mouse_pos=pygame.mouse.get_pos()
    choice=mouse_pos[1]//35-2
    if choice>=0 and choice<len(level):
        pygame.draw.rect(screen,(255,0,0),(SCREEN_W/4+28,70+35*choice,250,32),2)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
            if choice>=0 and choice<len(l):
                next_status=2
        if event.type == pygame.QUIT:
                next_status=-1
    return next_status,choice

#画像が存在しなかった場合
def no_image():
    screen.fill((255,255,255))
    txt=japanes.render("フォルダに画像を入れてください",True,(0,0,0))
    screen.blit(txt,(SCREEN_W/3+20,SCREEN_H/2))
    pygame.display.update()
    
# メイン
def main():
    status=0 #現在の処理
    bossflag=False
    title=pygame.image.load("system/title.png")
    title=pygame.transform.scale(title,(700,262))
    message_w=Message_Window()
    files=glob.glob("./image/*")
    files.sort()
    while True:
        clock.tick(60)
        if status==0:#メニュー画面
            status=menu(title)
        elif status==1:#難易度選択画面
            status,level=difficulty()
            if level==0:
                limit=5
            elif level==1:
                limit=10
            elif level==2:
                limit=20
            elif level==3:
                limit=50
            else:
                limit=9999
        elif status==2:#自機の画像選択画面
            now_level=1
            if len(files)==0:
                no_image()
                click()
                status=-1
            status,fin,img=get_image_file(files)
            if fin:
                me=color_read(img)
        elif status==3:#次のステージ移行処理
            if now_level%10 in [4,9]:#1の位が4か9のときに回復・技追加変更
                status=8
            elif now_level%10==0 or now_level==limit:#最終面か十の倍数面のときボス戦
                enemy=BOSS(now_level)
                status=4
                bossflag=True
            else:#それ以外は通常戦（敵はランダム生成）
                rnd=np.random.rand(8)
                col=[]
                for j,x in enumerate(rnd):
                    col.append(x/sum(rnd))
                    if j>=6:
                        col[np.random.randint(0,6)]+=col[j]
                if col.count(max(col))>1:
                    ind=[]
                    for j,ar in enumerate(col):
                        if j>=6:
                            continue
                        if ar==max(col):
                            ind.append(j)
                    max_color_num=np.random.choice(ind)
                else:
                    max_color_num=col.index(max(col))
                enemy=Enemy(what_is_color[max_color_num],col,now_level)
                status=4
        elif status==4:#バトル内わざ選択画面
            speed_check=True
            level_up_flag=True
            if type(enemy)==BOSS and bossflag:#ボス戦の場合最初だけ文字列表示
                screen.fill((255,255,255))
                me.draw()
                enemy.draw()
                enemy.name_draw()
                message_w.draw()
                pygame.draw.rect(screen,(255,255,0),(0,SCREEN_H/4,SCREEN_W,120),0)
                txt=bigjapanese.render("B O S S",True,(255,0,0))
                screen.blit(txt,(SCREEN_W/2-150,SCREEN_H/4+35))
                pygame.display.update()
                pygame.time.delay(1500)
                bossflag=False
            status,atk=battle_phase_choice(me,enemy,message_w)
        elif status==5:#バトル処理
            if speed_check:
                dmg_calc_me=True
                dmg_calc_en=True
                speed_check=False
                rnd=0
                my_speed=me.speed*(1+me.buff[2]/2)*(2/(2+me.debuff[2]))
                en_speed=enemy.speed*(1+enemy.buff[2]/2)*(2/(2+enemy.debuff[2]))
                if my_speed==en_speed:#スピードが同じならランダムで決定
                    rnd=np.random.randint(0,2)
                    if rnd==0:
                        rnd=-1
                my_speed+=rnd
                if my_speed>en_speed:
                    now_turn=1
                else:
                    now_turn=10
            if now_turn%10==1:#自分のターン
                if dmg_calc_en:#ダメージ計算
                    damage,batsugun_flag,buff_flag,debuff_flag=enemy.receive_damage(me.weapon[atk],me)
                    dmg_calc_en=False
                damage,fin_flag=battle_process(enemy,me,damage,batsugun_flag,buff_flag,debuff_flag,me,enemy,message_w,me.weapon[atk])
                if fin_flag:
                    click()
                    now_turn+=11
            elif now_turn//10==1:#相手のターン
                if dmg_calc_me:
                    e_choice=np.random.randint(0,len(enemy.weapon))
                    damage,batsugun_flag,buff_flag,debuff_flag=me.receive_damage(enemy.weapon[e_choice],enemy)
                    dmg_calc_me=False
                damage,fin_flag=battle_process(me,enemy,damage,batsugun_flag,buff_flag,debuff_flag,me,enemy,message_w,enemy.weapon[e_choice])
                if fin_flag:
                    click()
                    now_turn+=11
            if me.check_death() or enemy.check_death():#倒れたか
                click()
                status=6
            if now_turn==32 or now_turn==23:#両方のターン終了
                status=4
        elif status==6:#どちらかが倒れた（バトルが終了した）とき
            me.buff=[0,0,0]
            me.debuff=[0,0,0]
            screen.fill((255,255,255))
            me.draw()
            enemy.draw()
            enemy.name_draw()
            message_w.draw()
            if me.check_death():
                message_w.lose(me)
                status=11
            else:
                message_w.lose(enemy)
                if not now_level==limit:
                    status=7
                    now_level+=1
                else:
                    status=11
            pygame.display.update()
            click()
        elif status==7:#レベルアップ画面
            if level_up_flag:
                level_up_flag=False
                types=["HP","こうげき","ぼうぎょ","すばやさ"]
                hp_update_num=[10,30,50]
                update_num=[1,3,5]
                status_up=[]
                count=0
                while count<3:#強化要素はランダムで決定，被らないようにする
                    s=np.random.choice(types)
                    i=np.random.choice([0,1,2],p=[0.2,0.7,0.1])
                    if s=="HP":
                        x=[s,hp_update_num[i]]
                    else:
                        x=[s,update_num[i]]
                    if not x in status_up:
                        status_up.append(x)
                        count+=1
            status,x=level_up(me,status_up)
            if not status==7:
                me.status_up(status_up[x])
        elif status==8:#回復か技追加変更か選択画面
            status=choice(me)
            change=-1
            choiceflag=False
            imageflag=False
            chara=None
            if not status==8:
                now_level+=1
        elif status==9:#回復画面
            me.cure(100)
            screen.fill((255,255,255))
            message_w.draw()
            message_w.cure(me.name)
            pygame.display.update()
            status=3
            click()
        elif status==10:#技追加変更画面
            if len(me.weapon)==4 and not choiceflag:#わざを既に4つ覚えてる場合
                status,choiceflag,change=weaponchange_choice(me,message_w)
            elif not imageflag:#画像選択
                _,imageflag,image=get_image_file(files)
            else:#選択した画像からわざ決定
                if chara==None:
                    chara=color_read(image)
                status,w_choice=weaponchange(message_w,chara)
                if not status==10:
                    screen.fill((255,255,255))
                    message_w.draw()
                    if change==-1:
                        me.weapon.append(chara.weapon[w_choice])
                        message_w.w_add()
                    else:
                        me.weapon[change]=chara.weapon[w_choice]
                        message_w.w_change(change)
                    pygame.display.update()
                    click()
        elif status==11:#ゲーム終了
            screen.fill((255,255,255))
            message_w.draw()
            if me.check_death():#ゲームオーバー
                message_w.gameover()
                message_w.toutatu(now_level)
            else:#クリア
                message_w.clear()
            pygame.display.update()
            status=0
            click()
        else:#終了
            pygame.quit()
            sys.exit()



if __name__ == "__main__":
    main()