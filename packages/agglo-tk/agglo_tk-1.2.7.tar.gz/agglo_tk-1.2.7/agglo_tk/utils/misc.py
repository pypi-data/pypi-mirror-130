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

import inspect
from .time import AtkTimeoutChecker
from ..exceptions import AtkTimeoutError
from .trace import trace


def retry_on_failure(nb_retry=None, timeout_sec=None, retry_on=(Exception,), is_error_fatal=None, timeout_param="timeout_sec"):
    count_attempts = bool(nb_retry)

    def decorator(func):
        def wrapper(*args, **kwargs):
            result = None
            nonlocal timeout_sec

            # If retry is not steared by number of attempts
            if not count_attempts:
                func_signature = inspect.signature(func)

                # Force timeout_sec argument
                bound_args = func_signature.bind(*args, **kwargs)
                bound_args.apply_defaults()

                # Get timeout from decorated function parameters or from decorator parameters
                try:
                    timeout_sec_ = bound_args.arguments[timeout_param]
                    timeout_sec = timeout_sec_ or timeout_sec
                except KeyError:
                    pass
                timeout_checker = AtkTimeoutChecker(timeout_sec)

            while "function failed and retry allowed":
                try:
                    result = func(*args, **kwargs)
                    break
                # Case where one of the exception to be retried is raised
                except (retry_on) as error:
                    retry_msg = f"{func.__name__} failed on {repr(error)}, try again"

                    # If raised exception must not be retried
                    if is_error_fatal and is_error_fatal(error):
                        trace("ATK", info=f"fatal exception {repr(error)} can not be caught up, do not retry")
                        raise

                    # If retry is steared by number of attempts
                    if count_attempts:
                        if nb_retry <= 0:
                            raise error
                        nb_retry -= 1
                        trace("ATK", info=f"{retry_msg} ({nb_retry} attempts left)")
                    # If retry is steared by timeout
                    else:
                        try:
                            timeout_checker.check()
                            trace("ATK", info=f"{retry_msg} ({round(timeout_checker.remaining_sec, 2)} sec left)")
                        except AtkTimeoutError:
                            raise error
                except Exception as error:
                    trace("ATK", info=f"uncaught exception {repr(error)}, do not retry")
                    raise

            return result

        return wrapper
    return decorator
