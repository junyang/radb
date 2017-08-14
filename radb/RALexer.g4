lexer grammar RALexer;

WS : [ \n\t\r]+ -> skip;
COMMENT : '/*' (COMMENT|.)*? '*/' -> skip;
LINE_COMMENT : '//' .*? '\n' -> skip;
TERMINATOR : ';';
FORCE : '!';

IS_NULL : IS WS NULL;
IS_NOT_NULL : IS WS NOT WS NULL;
IS : I S;
NULL : N U L L;
LIKE : L I K E;
AND : A N D;
OR : O R;
NOT : N O T;

STRING : '\'' (~('\'' | '\r' | '\n') | '\'\'' | ('\r'? '\n'))* '\'';
NUMBER : UNSIGNED_INTEGER_FRAGMENT* '.'? UNSIGNED_INTEGER_FRAGMENT+;
ID : ('a'..'z' | 'A'..'Z' | '_') ('a'..'z' | 'A'..'Z' | '_' | '0'..'9')*;

RENAME : '\\rename';
PROJECT : '\\project';
SELECT : '\\select';
JOIN : '\\join';
CROSS : '\\cross';
UNION : '\\union';
DIFF : '\\diff';
INTERSECT : '\\intersect';

DOT : '.';
COMMA : ',';
STAR : '*';
SLASH : '/';
PLUS : '+';
MINUS : '-';
CONCAT : '||';
PAREN_L : '(';
PAREN_R : ')';
ARG_L : '_{';
ARG_R : '}';

GETS : ':-';
COLON: ':';
LE: '<=';
NE: '<>';
GE: '>=';
LT: '<';
EQ: '=';
GT: '>';
LIST : '\\list';
CLEAR : '\\clear';
SAVE : '\\save';
SOURCE : '\\source';
QUIT : '\\quit';
SQLEXEC : '\\sqlexec' -> pushMode(SQLEXEC_MODE);

fragment A : [aA];
fragment B : [bB];
fragment C : [cC];
fragment D : [dD];
fragment E : [eE];
fragment F : [fF];
fragment G : [gG];
fragment H : [hH];
fragment I : [iI];
fragment J : [jJ];
fragment K : [kK];
fragment L : [lL];
fragment M : [mM];
fragment N : [nN];
fragment O : [oO];
fragment P : [pP];
fragment Q : [qQ];
fragment R : [rR];
fragment S : [sS];
fragment T : [tT];
fragment U : [uU];
fragment V : [vV];
fragment W : [wW];
fragment X : [xX];
fragment Y : [yY];
fragment Z : [zZ];
fragment UNSIGNED_INTEGER_FRAGMENT : ('0'..'9')+;

mode SQLEXEC_MODE;
SQLEXEC_TEXT : WS? ARG_L
( ('\'' (~('\'' | '\r' | '\n') | ('\r'? '\n'))* '\'') |
  ('"' (~('"' | '\r' | '\n') | ('\r'? '\n'))* '"') |
  ~('\''|'"') )*? ARG_R -> popMode;
