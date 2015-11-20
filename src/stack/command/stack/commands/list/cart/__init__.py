# @SI_Copyright@
#                             www.stacki.com
#                                  v2.0
# 
#      Copyright (c) 2006 - 2015 StackIQ Inc. All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#  
# 1. Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#  
# 2. Redistributions in binary form must reproduce the above copyright
# notice unmodified and in its entirety, this list of conditions and the
# following disclaimer in the documentation and/or other materials provided 
# with the distribution.
#  
# 3. All advertising and press materials, printed or electronic, mentioning
# features or use of this software must display the following acknowledgement: 
# 
# 	 "This product includes software developed by StackIQ" 
#  
# 4. Except as permitted for the purposes of acknowledgment in paragraph 3,
# neither the name or logo of this software nor the names of its
# authors may be used to endorse or promote products derived from this
# software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY STACKIQ AND CONTRIBUTORS ``AS IS''
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL STACKIQ OR CONTRIBUTORS
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN
# IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# @SI_Copyright@

import os
import stat
import time
import sys
import string
import stack.commands


class Command(stack.commands.CartArgumentProcessor,
	stack.commands.list.command):
	"""
	List the status of available carts.
	
	<arg optional='1' type='string' name='cart' repeat='1'>
	List of carts. This should be the cart base name (e.g., stacki, os,
	etc.). If no carts are listed, then status for all the carts are
	listed.
	</arg>

	<example cmd='list cart kernel'>		
	List the status of the kernel cart.
	</example>
	
	<example cmd='list cart'>
	List the status of all the available carts.
	</example>
	"""		

	def run(self, params, args):
		self.beginOutput()

		try:
			carts = self.getCartNames(args, params)
		except:
			carts = []

		for cart in carts:
                    
			# For each cart determine if it is enabled
			# in any box.
                        
                        boxes = []

                        for row in self.db.select("""b.name from
                                cart_stacks s, carts c, boxes b where
                                c.name='%s' and
                                s.cart=c.id and s.box=b.id """
				% cart):

                        	boxes.append(row[0])
			
			self.addOutput(cart, string.join(boxes,' '))

		self.endOutput(header=['name', 'boxes'], trimOwner=False)

