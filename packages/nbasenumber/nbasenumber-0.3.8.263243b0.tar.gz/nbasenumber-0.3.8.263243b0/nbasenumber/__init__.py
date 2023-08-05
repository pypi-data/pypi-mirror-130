#!/usr/bin/env python3
# coding-UTF-8

class Base(object) :
    """Create a mathematical integral number with n base.
  Base(num_base=10, digits=(), is_negative=False)
  e.g.
    Base(10, (1, 0, 4, 8, 5, 7, 6))
    Base(2, (1, 0, 0, 0, 1, 0, 1))
    Base(16, (12, 8, 9, 11, 15, 0, 1, 5), True)
"""
    
    def __init__(self, num_base=10, digits=(), is_negative=False) :
        try :
            num_base.__Base__
        except AttributeError :
            if type(num_base) != type(0) :
                raise TypeError("num_base must be an int, not "+\
                                str(type(num_base)))
            if num_base < 2 :
                raise ValueError("num_base must be greater than 1, got "+\
                                 str(num_base))
            self.__num_base = num_base
            digits = tuple(digits)
            for i in digits :
                if type(i) != type(0) :
                    raise TypeError("value in digits must be an int, not "+\
                                    str(type(i)))
                if i < 0 :
                    raise ValueError("value in digits must be greater than -1, \
got "+str(num_base))
                if i >= num_base :
                    raise ValueError("value in digits must be less than "+\
                                     str(num_base)+", got "+str(num_base))
            self.__digits = digits
            if is_negative and digits != () :
                self.__is_negative = True
            else :
                self.__is_negative = False
        else :
            self.__num_base = num_base.__Base__().__num_base
            self.__digits = num_base.__Base__().__digits
            self.__is_negative = num_base.__Base__().__is_negative
    @property
    def num_base(self) :
        return self.__num_base
    @property
    def digits(self) :
        return self.__digits
    @property
    def is_negative(self) :
        return self.__is_negative
    
    def __repr__(self) :
        return "Base(%d, %s, %s)" % (self.__num_base, str(self.__digits),
                                     str(self.__is_negative))
    
    def __int__(self) :
        res = 0
        place = 0
        for i in self.digits[::-1] :
            res += i * self.num_base ** place
            place += 1
        if self.is_negative :
            return -res
        return res
    
    def __bool__(self) :
        return self.__digits != ()
    
    def __float__(self) :
        return float(int(self))
    
    def __abs__(self) :
        return Base(self.__num_base, self.__digits)
    
    def __pos__(self) :
        return Base(self.__num_base, self.__digits, self.__is_negative)
    
    def __neg__(self) :
        return Base(self.__num_base, self.__digits, not(self.__is_negative))
    
    def __hash__(self) :
        return hash(int(self))
    
    def __eq__(self, value) :
        if type(value) == Base :
            return int(self) == int(value)
        elif type(value) == type(0) :
            return int(self) == value
        else :
            try :
                return int(self) == float(value)
            except Exception :
                return False
    
    def __ne__(self, value) :
        if type(value) == Base :
            return int(self) != int(value)
        elif type(value) == type(0) :
            return int(self) != value
        else :
            try :
                return int(self) != float(value)
            except Exception :
                return True
    
    def __gt__(self, value) :
        if type(value) == Base :
            return int(self) > int(value)
        elif type(value) == type(0) :
            return int(self) > value
        else :
            try :
                return int(self) > float(value)
            except Exception :
                return NotImplemented
    
    def __lt__(self, value) :
        if type(value) == Base :
            return int(self) < int(value)
        elif type(value) == type(0) :
            return int(self) < value
        else :
            try :
                return int(self) < float(value)
            except Exception :
                return NotImplemented
    
    def __ge__(self, value) :
        if type(value) == Base :
            return int(self) >= int(value)
        elif type(value) == type(0) :
            return int(self) >= value
        else :
            try :
                return int(self) >= float(value)
            except Exception :
                return NotImplemented
    
    def __le__(self, value) :
        if type(value) == Base :
            return int(self) <= int(value)
        elif type(value) == type(0) :
            return int(self) <= value
        else :
            try :
                return int(self) <= float(value)
            except Exception :
                return NotImplemented
    
    def __add__(self, value) :
        if type(value) == Base :
            d_int = abs(int(self)+int(value))
            m_digits = ()
            while d_int != 0 :
                m_digits = (d_int%self.__num_base,) + m_digits
                try :
                    raw_input # check for Python 2 or Python 3
                except NameError :
                    d_int = eval("d_int // self.num_base")
                else :
                    d_int = eval("d_int / self.num_base")
            return Base(self.__num_base, m_digits, int(self)+int(value)<0)
        else :
            if type(value) != type(0) :
                return NotImplemented
            d_int = abs(int(self)+value)
            m_digits = ()
            while d_int != 0 :
                m_digits = (d_int%self.__num_base,) + m_digits
                try :
                    raw_input # check for Python 2 or Python 3
                except NameError :
                    d_int = eval("d_int // self.num_base")
                else :
                    d_int = eval("d_int / self.num_base")
            return Base(self.__num_base, m_digits, int(self)+value<0)
    
    def __sub__(self, value) :
        return self + -value
    
    def __mul__(self, value) :
        if type(value) == Base :
            d_int = abs(int(self)*int(value))
            m_digits = ()
            while d_int != 0 :
                m_digits = (d_int%self.__num_base,) + m_digits
                try :
                    raw_input # check for Python 2 or Python 3
                except NameError :
                    d_int = eval("d_int // self.num_base")
                else :
                    d_int = eval("d_int / self.num_base")
            return Base(self.__num_base, m_digits, int(self)*int(value)<0)
        else :
            if type(value) != type(0) :
                return NotImplemented
            d_int = abs(int(self)*value)
            m_digits = ()
            while d_int != 0 :
                m_digits = (d_int%self.__num_base,) + m_digits
                try :
                    raw_input # check for Python 2 or Python 3
                except NameError :
                    d_int = eval("d_int // self.num_base")
                else :
                    d_int = eval("d_int / self.num_base")
            return Base(self.__num_base, m_digits, int(self)*value<0)
    
    def __truediv__(self, value) :
        try :
            return float(self) / float(value)
        except Exception :
            return NotImplemented
    
    def __floordiv__(self, value) :
        if type(value) == Base :
            try :
                raw_input # check for Python 2 or Python 3
            except NameError :
                d_int = eval("abs(int(self)//int(value))")
            else :
                d_int = eval("abs(int(self)/int(value))")
            m_digits = ()
            while d_int != 0 :
                m_digits = (d_int%self.__num_base,) + m_digits
                try :
                    raw_input # check for Python 2 or Python 3
                except NameError :
                    d_int = eval("d_int // self.num_base")
                else :
                    d_int = eval("d_int / self.num_base")
            return Base(self.__num_base, m_digits, int(self)*int(value)<0)
        else :
            if type(value) == type(0) :
                try :
                    raw_input # check for Python 2 or Python 3
                except NameError :
                    d_int = eval("abs(int(self)//value)")
                else :
                    d_int = eval("abs(int(self)/value)")
            else :
                try :
                    try :
                        raw_input # check for Python 2 or Python 3
                    except NameError :
                        d_int = eval("abs(int(int(self)//float(value)))")
                    else :
                        d_int = eval("abs(int(int(self)/float(value)))")
                except Exception :
                    return NotImplemented
            m_digits = ()
            while d_int != 0 :
                m_digits = (d_int%self.__num_base,) + m_digits
                try :
                    raw_input # check for Python 2 or Python 3
                except NameError :
                    d_int = eval("d_int // self.num_base")
                else :
                    d_int = eval("d_int / self.num_base")
            return Base(self.__num_base, m_digits, int(self)*value<0)
    
    def __mod__(self, value) :
        if type(value) == Base :
            d_int = abs(int(self)%int(value))
            m_digits = ()
            while d_int != 0 :
                m_digits = (d_int%self.__num_base,) + m_digits
                try :
                    raw_input # check for Python 2 or Python 3
                except NameError :
                    d_int = eval("d_int // self.num_base")
                else :
                    d_int = eval("d_int / self.num_base")
            return Base(self.__num_base, m_digits, int(self)%int(value)<0)
        else :
            if type(value) != type(0) :
                return NotImplemented
            d_int = abs(int(self)%value)
            m_digits = ()
            while d_int != 0 :
                m_digits = (d_int%self.__num_base,) + m_digits
                try :
                    raw_input # check for Python 2 or Python 3
                except NameError :
                    d_int = eval("d_int // self.num_base")
                else :
                    d_int = eval("d_int / self.num_base")
            return Base(self.__num_base, m_digits, int(self)%value<0)
    
    def __pow__(self, value, mod=None) :
        if type(value) == Base :
            if mod == None :
                d_int = int(self) ** int(value)
            elif type(mod) == Base :
                d_int = int(self) ** int(value) % int(mod)
            elif type(mod) == type(0) :
                d_int = int(self) ** int(value) % mod
            else :
                return NotImplemented
            i_n = d_int < 0
            d_int = abs(d_int)
            m_digits = ()
            while d_int != 0 :
                m_digits = (d_int%self.__num_base,) + m_digits
                try :
                    raw_input # check for Python 2 or Python 3
                except NameError :
                    d_int = eval("d_int // self.num_base")
                else :
                    d_int = eval("d_int / self.num_base")
            return Base(self.__num_base, m_digits, i_n)
        else :
            if type(value) != type(0) :
                return NotImplemented
            if mod == None :
                d_int = int(self) ** value
            elif type(mod) == Base :
                d_int = int(self) ** value % int(mod)
            elif type(mod) == type(0) :
                d_int = int(self) ** value % mod
            else :
                return NotImplemented
            i_n = d_int < 0
            d_int = abs(d_int)
            m_digits = ()
            while d_int != 0 :
                m_digits = (d_int%self.__num_base,) + m_digits
                try :
                    raw_input # check for Python 2 or Python 3
                except NameError :
                    d_int = eval("d_int // self.num_base")
                else :
                    d_int = eval("d_int / self.num_base")
            return Base(self.__num_base, m_digits, i_n)
    
    def __divmod__(self, value) :
        return (self.__floordiv__(value), self%value)
    
    def __and__(self, value) :
        if type(value) == Base :
            d_int = abs(int(self)&int(value))
            m_digits = ()
            while d_int != 0 :
                m_digits = (d_int%self.__num_base,) + m_digits
                try :
                    raw_input # check for Python 2 or Python 3
                except NameError :
                    d_int = eval("d_int // self.num_base")
                else :
                    d_int = eval("d_int / self.num_base")
            return Base(self.__num_base, m_digits, int(self)&int(value)<0)
        else :
            if type(value) != type(0) :
                return NotImplemented
            d_int = abs(int(self)&value)
            m_digits = ()
            while d_int != 0 :
                m_digits = (d_int%self.__num_base,) + m_digits
                try :
                    raw_input # check for Python 2 or Python 3
                except NameError :
                    d_int = eval("d_int // self.num_base")
                else :
                    d_int = eval("d_int / self.num_base")
            return Base(self.__num_base, m_digits, int(self)&value<0)
    
    def __or__(self, value) :
        if type(value) == Base :
            d_int = abs(int(self)|int(value))
            m_digits = ()
            while d_int != 0 :
                m_digits = (d_int%self.__num_base,) + m_digits
                try :
                    raw_input # check for Python 2 or Python 3
                except NameError :
                    d_int = eval("d_int // self.num_base")
                else :
                    d_int = eval("d_int / self.num_base")
            return Base(self.__num_base, m_digits, int(self)|int(value)<0)
        else :
            if type(value) != type(0) :
                return NotImplemented
            d_int = abs(int(self)|value)
            m_digits = ()
            while d_int != 0 :
                m_digits = (d_int%self.__num_base,) + m_digits
                try :
                    raw_input # check for Python 2 or Python 3
                except NameError :
                    d_int = eval("d_int // self.num_base")
                else :
                    d_int = eval("d_int / self.num_base")
            return Base(self.__num_base, m_digits, int(self)|value<0)
    
    def __xor__(self, value) :
        if type(value) == Base :
            d_int = abs(int(self)^int(value))
            m_digits = ()
            while d_int != 0 :
                m_digits = (d_int%self.__num_base,) + m_digits
                try :
                    raw_input # check for Python 2 or Python 3
                except NameError :
                    d_int = eval("d_int // self.num_base")
                else :
                    d_int = eval("d_int / self.num_base")
            return Base(self.__num_base, m_digits, int(self)^int(value)<0)
        else :
            if type(value) != type(0) :
                return NotImplemented
            d_int = abs(int(self)^value)
            m_digits = ()
            while d_int != 0 :
                m_digits = (d_int%self.__num_base,) + m_digits
                try :
                    raw_input # check for Python 2 or Python 3
                except NameError :
                    d_int = eval("d_int // self.num_base")
                else :
                    d_int = eval("d_int / self.num_base")
            return Base(self.__num_base, m_digits, int(self)^value<0)
    
    def __not__(self) :
        return -self - 1
    
    def __invert__(self) :
        return -self - 1
    
    def __round__(self, ndigits=None) :
        """Round self as a decimal."""
        
        if type(ndigits) == Base :
            ndigits = int(ndigits)
        elif ndigits == None or type(ndigits) == type(0) :
            pass
        else :
            return NotImplemented
        d_int = abs(round(int(self), ndigits))
        m_digits = ()
        while d_int != 0 :
            m_digits = (d_int%self.__num_base,) + m_digits
            try :
                raw_input # check for Python 2 or Python 3
            except NameError :
                d_int = eval("d_int // self.num_base")
            else :
                d_int = eval("d_int / self.num_base")
        return Base(self.__num_base, m_digits, round(int(self), ndigits)<0)
