############################################################################
##
## Copyright (C) 2025 Plaisic and/or its subsidiary(-ies).
## Contact: eti.laurent@gmail.com
##
## This file is part of the Agglo project.
##
## AGGLO_BEGIN_LICENSE
## Commercial License Usage
## Licensees holding valid commercial Agglo licenses may use this file in
## accordance with the commercial license agreement provided with the
## Software or, alternatively, in accordance with the terms contained in
## a written agreement between you and Plaisic.  For licensing terms and
## conditions contact eti.laurent@gmail.com.
##
## GNU General Public License Usage
## Alternatively, this file may be used under the terms of the GNU
## General Public License version 3.0 as published by the Free Software
## Foundation and appearing in the file LICENSE.GPL included in the
## packaging of this file.  Please review the following information to
## ensure the GNU General Public License version 3.0 requirements will be
## met: http://www.gnu.org/copyleft/gpl.html.
##
## In addition, the following conditions apply:
##     * Redistributions in binary form must reproduce the above copyright
##       notice, this list of conditions and the following disclaimer in
##       the documentation and/or other materials provided with the
##       distribution.
##     * Neither the name of the Agglo project nor the names of its
##       contributors may be used to endorse or promote products derived
##       from this software without specific prior written permission.
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
## "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
## LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
## A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
## OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
## SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
## TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
## PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
## LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
## NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
## SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
##
## AGGLO_END_LICENSE
##
############################################################################

__all__ = ["AtkError", "AtkUndecidedError", "AtkTimeoutError", "AtkSelectorError", "AtkIOSelectorError", 
           "AtkIOHubError", "AtkIODeviceError", "AtkLimitedAccessError", "AtkNotFriendError"]

class AtkError(Exception):
    MSG = "{op} error: {msg}"

    def __init__(self, *args, **kwargs):
        subtype = args[0] if args else self.MSG

        super().__init__(subtype.format(**kwargs))
        self.__subtype = subtype
        self.__attrs = kwargs


    def __getattr__(self, attr_name):
        try:
            return self.__attrs[attr_name]
        except KeyError:
            raise AttributeError(f"'{type(self).__name__}' object '{attr_name}' attribute is not set")


    def __repr__(self):
        # subtype = f"'{self.subtype}', " if self.subtype else ""
        result = ""
        subtype = ""
        cls = type(self)
        cls_name = cls.__name__
        attrs = ', '.join(f"{name}={repr(value)}" for name, value in self.__attrs.items())

        # Retrieve subtype
        if self.subtype:
            try:
                subtypes = vars(cls)
                subtype_name = list(subtypes.keys())[list(subtypes.values()).index(self.subtype)]

                subtype = f"{cls_name}.{subtype_name}, "
            # Case where subtype is not a class attribute
            except ValueError:
                subtype = f"{repr(self.subtype)}, "

        result = f"{cls_name}({subtype}{attrs})"
        
        return result
        

    @property
    def subtype(self):
        result = self.__subtype if (self.__subtype != self.MSG) else None

        return result
        

class AtkUndecidedError(ValueError, AtkError):
    MSG = "no %s defined in data to match"


class AtkTimeoutError(AtkError):
    MSG = "Fail to execute {op} within {timeout_sec} sec"


class AtkSelectorError(AtkError):
    MSG = "Searching for {nb_searched} elements failed, {nb_found} found"
    
    def __init__(self, selector, found_ios, nb_searched):
        super(AtkSelectorError, self).__init__(nb_searched=nb_searched, nb_found=len(found_ios))
        self.selector = selector
        self.found_ios = found_ios


class AtkIOSelectorError(AtkSelectorError):
    MSG = "Negative rank %s used for match, total number of ios unknown "
    
    def __init__(self, selector):
        # TODO revoir l'heritage
        # super(AtkIOSelectorError, self).__init__(selector, None)
        self.selector = selector
        AtkError.__init__(self)
        # TODO
        # self.message = AtkIOSelectorError.MSG


class AtkIOHubError(ValueError, AtkError):
    UNKNOWN_DEVICE = "io device isn't managed by io hub"
    CONFLICT = "io device is managed outside of io hub's scope"


# TODO heriter de IOError ?
class AtkIODeviceError(ValueError, AtkError):
    NOT_OPENED = "io device is not opened"
    ALREADY_OPENED = "io device is already opened"


class AtkLimitedAccessError(AttributeError, AtkError):
    MASKED = "%s is masked by proxy"
    CONFLICT = "name %s is already used"
    CANNOT_SET_REF = "can't set reference %s"
    CANNOT_DEL_REF = "can't delete reference %s"


class AtkNotFriendError(AtkError):
    MSG = "not a friend"


class AtkDynamicClassError(AtkError):
    NEW_OVERRIDEN = "Do not use overriden __new__ in conjunction with AtkDynamicClassError"
    MULTI_PARENT = "Do not multi heritate from AtkDynamicClassError"
