# -*- coding: utf-8 -*-
"""
Created on Thu Jun 16 10:06:58 2022

@author: Patrick
"""

class CommentYaccer:
    tokens = (
        'commentLine',
        'commentBlockStart',
        'commentBlockEnd',
        'anyTextLine',
        'anyTextMultiLine'
    )
         
    # Regular expression rules for simple tokens
    t_commentLine = r'//'
    t_commentBlockStart = r'/*'
    t_commentBlockEnd = r'*/'
    t_anyTestLine = r'[a-zA-Z]+'
    t_anyTextMultiLine = r'((.|\n)*)'
    
    
    
    