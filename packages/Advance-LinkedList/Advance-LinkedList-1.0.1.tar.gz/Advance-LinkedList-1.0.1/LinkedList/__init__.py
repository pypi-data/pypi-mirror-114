# version of a module
__version__="1.0.1"
__author__="Nitin Gupta"
class LinkedList:
    def __init__(self,Iterable:object="",initialize_list:bool=False,size:int=0,initial_value:object=0,sorted:bool=False,order:bool=False,dtype:object=None)->None:
        self.next=None
        self.dtype=dtype
        self.mode=sorted
        self.__last=self
        self.order=order
        self.__length=0
        self.__data=0
        if(initialize_list):
            for item in range(size):
                self.append(initial_value)
        else:
            for item in Iterable:
                self.append(item)
    def append(self,data:object=0)->None:
        self.__length+=1
        tem=LinkedList()
        if(self.__dtype!=None):
            data=self.__dtype(data)
        tem.__data = data
        t=self
        if(self.__mode):
            while(t.next!=None and ((t.next.__data<data and not self.__order) or (t.next.__data>data and self.__order))):
                t=t.next
            tem.next=t.next
            t.next=tem
        else:
            tem.__last=self.__last
            self.__last.next=tem
            self.__last=tem
    def __str__(self):
        a="[ "
        t=self.next
        while(t!=None):
            if(isinstance(t.__data,str)):
                a+=f"'{t.__data}' ,"
            else:
                a+=f"{t.__data} ,"
            t=t.next
        a+="\b]"
        return a
    def __len__(self):
        return self.__length
    def extend(self,_iterable):
        for item in _iterable:
            self.append(item)
    def copy(self):
        tem=LinkedList()
        t=self.next
        while(t!=None):
            tem.append(t.__data)
            t=t.next
        return tem
    def insert_index(self,index:int,data:object):
        self.__length+=1
        tem=LinkedList()
        tem.__data=data
        i=0
        t=self
        while(t!=None):
            if(i==index or i==self.__length-1):
                tem.next=t.next
                t.next=tem
                break
            i+=1
            t=t.next
    def __getitem__(self, item):
        if(not isinstance(item,int) and not isinstance(item,LinkedList)):
            a=item.start
            b=item.stop
            c=item.step
            if (c == None):
                c = 1
            if(a==None):
                if(c>=0):
                    a=0
                else:
                    a=len(self)
            if(b==None):
                if(c>=0):
                    b=len(self)
                else:
                    b=-1
            tem=LinkedList()
            t=self
            if(a<-len(self) or a>len(self) or b>len(self) or b<-len(self) ):
                raise IndexError("Index out of range")
            else:
                var1=0
                if(c<0):
                    a,b=b+1,a+1
                    c=-1*c
                    var1=-1
                i=0
                while(t!=None):
                    if(i==a):
                        break
                    i+=1
                    t=t.next
                t=t.next
                k=i
                while(t!=None and i<b):
                    if(k==i):
                        tem.append(t.__data)
                        k+=(c)
                    t=t.next
                    i+=1
                if(var1==-1):
                    tem.reversed()
            return tem
        elif(isinstance(item,LinkedList)):
            return item.next.__data
        else:
            if(item<0):
                if(item<-len(self)):
                    raise IndexError("Index out of range")
                else:
                    item=len(self)+item
            else:
                if(item>len(self)):
                    raise IndexError("Index out of range")
            t=self
            i=0
            while(t.next!=None):
                if(i==item):
                    return t.next.__data
                t=t.next
                i+=1
            raise StopIteration
    def __setitem__(self, key, value):
        if(isinstance(key,int)):
            t=self
            i=0
            while(t.next!=None):
               if(i==key):
                   t.next.__data=value
                   break
               t=t.next
               i+=1
        else:
            try:
                key.next.__data=value
            except:
                raise SyntaxError("Invalid reffernce pass for Linked list assignment")
    def insert_reffernce(self,obj:object,data:object)->None:
        self.__length+=1
        tem=LinkedList()
        tem.__data=data
        tem.next=obj.next
        obj.next=tem
    def swap(self,obj1:object,obj2:object):
            self[obj1],self[obj2]=self[obj2],self[obj1]
    def __reversed__(self):
        t=self.copy()
        t.reversed()
        return t
    def reversed(self):
        t=self.next
        if(t!=None):
            p=self.next.next
            t.next=None
            while(p!=None):
                q=p.next
                p.next=t
                t=p
                p=q
            self.next=t
    def __eq__(self, other):
        self=other
    def __mul__(self, other:int):
        if(isinstance(other,int)):
            if(other==1):
                return self
            else:
                return self+self.__mul__(other-1)
        else:
            raise SyntaxError(f"Invalid operator between Linked list object and {type(other).__name__} object")

    def __add__(self, other):
        if(isinstance(other,LinkedList)):
            tem=LinkedList(self)
            t=other.next
            while(t!=None):
                tem.append(t.__data)
                t=t.next
            return tem
        else:
            raise SyntaxError("Invalid operator between linked list and %s" % (type(other).__name__))
    def __abs__(self):
        t = self
        while (t.next != None):
            if (isinstance(t.next.__data, int) or isinstance(t.next.__data, float)):
                t.next.__data = abs(t.next.__data)
            t = t.next
    def Sum(self):
        return sum(self)
    def mean(self):
        return sum(self)/len(self)
    def meadian(self):
        # Mode = 3(Median) - 2(Mean) use this relation to compute median in o(n)
        ans="%.1f"%((self.mode()+(2*self.mean()))/3)
        return float(ans)
    def mode(self):
        d={}
        for item in self:
            if(item in d):
                d[item]+=1
            else:
                d[item]=1
        max=list(d.keys())
        max=max[0]
        for item in d:
            if(d[item]>d[max] and d[item]>1):
                max=item
        l=0
        s=0
        for item in d:
            if(d[item]==d[max]):
                s+=item
                l+=1
        return (s/l)
    def __pow__(self, power,modula=None):
        t = self
        while (t.next != None):
            if (isinstance(t.next.__data, int) or isinstance(t.next.__data, float)):
                t.next.__data = pow(t.next.__data,power,modula)
            t = t.next
    @classmethod
    def create_sized_list(cls,size=0,intial_value=0):
        tem=LinkedList()
        tem.__length=size
        for item in range(size):
            tem.append(intial_value)
        return tem
    def sqrt(self,modula=None):
        t=self
        self.__pow__(0.5,modula)
    def count(self,element,start=0,end=-1):
        if(end==-1):
            end=len(self)
        count=0
        t=self
        i=0
        while(t!=None):
            if(i>=start):
                if(t.next.__data==element):
                    count+=1
            i+=1
            if(i==end):
                break
            t=t.next
        return count
    def index(self,value,start=0,end=-1):
        if(end==-1):
            end=len(self)
        t = self
        i = 0
        while (t != None):
            if (i >= start):
                if (t.next.__data == value):
                    return i
            i += 1
            t=t.next
            if (i == end):
                break
        return -1
    def pop(self,index=-1):
        if(index==-1):
            index=len(self)-1
        t=self
        i=0
        while(t.next!=None):
            if(i==index):
                t.next=t.next.next
                break
            t=t.next
            i+=1
        self.__length-=1
    def serarch(self,value:object)->bool:
        return self.index(value)!=-1
    def remove(self,value):
        j=self.index(value)
        if(j!=-1):
            self.pop(j)
    def clear(self):
        self.__length=0
        self.next=None
    def __iadd__(self, other):
        if(isinstance(other,LinkedList)):
            t=other
            while(t.next!=None):
                self.append(t.next.__data)
                t=t.next
            return self
        else:
            raise SyntaxError("Invalid operator between linked list and %s"%(type(other).__name__))
    def __imul__(self, other):
        return self.__mul__(other)
    def __call__(self, *args, **kwargs):
        for item in args:
            self.append(item)
    def replace(self,old_value,new_value,times=-1):
        count=0
        t=self
        while(t.next!=None):
            if(count==times):
                break
            if(t.next.__data==old_value):
                count+=1
                t.next.__data=new_value
            t=t.next
    def rindex(self,value):
        t=self
        i=0
        j=-1
        while(t.next!=None):
            if(t.next.__data==value):
                j=i
            i+=1
            t=t.next
        return j
    def concatenate(self,item=""):
        t=self
        ans=""
        while(t.next!=None):
            ans+=str(t.next.__data)
            ans+=item
            t=t.next
        return ans
    def partition(self,value:int,starts:object=0,ends:object=-1):
        if(isinstance(starts,int) and isinstance(ends,int)):
            startp=self
            midp=self
            endp=self.__last.__last
        else:
            startp = starts
            midp = starts
            endp = ends
        mid=0
        end=len(self)-1
        while(end>=mid and midp.next!=endp.next):
            if(midp.next.__data>value):
                endp.next.__data,midp.next.__data=midp.next.__data,endp.next.__data
                end-=1
                endp=endp.__last
            elif(midp.next.__data<value):
                startp.next.__data,midp.next.__data=midp.next.__data,startp.next.__data
                startp=startp.next
                midp=midp.next
                mid+=1
            else:
                midp = midp.next
                mid += 1
        return (startp,endp.next)
    def cummulativeSum(self):
        tem=LinkedList([0])
        sum=0
        t=self
        while(t.next!=None):
            if(isinstance(t.next.__data,int) or isinstance(t.next.__data,float)):
                sum+=t.next.__data
                tem.append(sum)
            t=t.next
        return tem
    def Max(self):
        return max(self)
    def Min(self):
        return min(self)
    def join(self,item):
        t=self
        while(t.next!=None):
            self.insert_reffernce(t.next,item)
            t=t.next.next
    def maxSum(self):
        sum=0
        t=self
        try:
            ans=t.next.__data
        except:
            ans=0
        while(t.next!=None):
            if (isinstance(t.next.__data, int) or isinstance(t.next.__data, float)):
                sum+=(t.next.__data)
                if(sum<0):
                    sum=0
                ans = max(ans, sum)
            t=t.next
        return ans
    def maxProduct(self):
        t = self
        try:
            max1 = t.next.__data
            max2 = t.next.__data
            min1 = t.next.__data
            min2 = -t.next.__data
        except:
            min1 = 0
            max1 = 0
            max2 = 0
            min2 = 0
        while (t.next != None):
            if (isinstance(t.next.__data, int) or isinstance(t.next.__data, float)):
                if(max1<t.next.__data):
                    max1=t.next.__data
                elif(max2<t.next.__data and t.next.__data<=max1):
                    max2=t.next.__data
                else:
                    pass
                if(min1>=t.next.__data):
                    min1=t.next.__data
                elif (min2 >= t.next.__data and t.next.__data>=min1):
                    min2 = t.next.__data
            t = t.next
        if(min1*min2>max2*max1):
            return (min1*min2,(min1,min2))
        return (max1*max2,(max1,max2))
    def shift(self,value,side=True):
        startp = self
        midp = self
        endp = self.__last.__last
        mid = 0
        end = len(self) - 1
        while (end >= mid and midp.next != None):
            if (midp.next.__data!=value and side):
                endp.next.__data, midp.next.__data = midp.next.__data, endp.next.__data
                end -= 1
                endp = endp.__last
            elif (midp.next.__data!=value and not side):
                startp.next.__data, midp.next.__data = midp.next.__data, startp.next.__data
                startp = startp.next
                midp = midp.next
                mid += 1
            else:
                midp = midp.next
                mid += 1
    def __fact(self,n):
        a=1
        for i in range(2,n+1):
            a*=i
        return a
    def factorial(self):
        t = self
        while (t.next != None):
            if (isinstance(t.next.__data, int) or isinstance(t.next.__data, float)):
                t.next.__data=self.__fact(t.next.__data)
            t = t.next
    def sort(self,order:bool=False):
        tem=LinkedList(sorted(self,reverse=order))
        t=self
        while(t.next!=None):
            t.next.__data=tem.next.__data
            tem=tem.next
            t=t.next
    def power(self,power,modula=None):
        self.__pow__(power,modula)