grammar Grammar;

start : expr ; 

expr  : '(' expr ')'                                                                                                              #parenExpr 
      | op='#' param=expr                                                                                                         #paramExpr 
      | op=('TrendSecond'|'Trend'|'Avg'|'Median') '(' param=expr ',' time=expr ')'                                                #paramExpr 
      | op=('Integral'|'IntegralLebesgue') '(' param=expr ',' time=expr ',' reference=expr ',' below=expr ',' exponent=expr ')'   #paramExpr 
      | op=('Round'|'Str') '(' value=expr ',' decimals=expr ')'                                                                   #roundExpr 
      | left=expr op='^' right=expr                                                                                               #mathExpr 
      | op=('sqr2'|'sqr3'|'Abs') '(' right=expr ')'                                                                               #mathExpr 
      | left=expr op=('*'|'/') right=expr                                                                                         #mathExpr 
      | left=expr op=('+'|'-') right=expr                                                                                         #mathExpr 
      | op=('+'|'-') right=expr                                                                                                   #mathExpr 
      | left=expr op=('AND'|'OR') right=expr                                                                                      #boolExpr 
      | op='NOT' right=expr                                                                                                       #boolExpr 
      | left=expr op='_' right=expr                                                                                               #concatExpr 
      | left=expr op=('>'|'>='|'<'|'<='|'='|'!=') right=expr                                                                      #comparExpr 
      | 'If(' check=expr ',' isTrue=expr ',' isFalse=expr ')'                                                                     #ifExpr 

      | 'Advisory(' check=expr ',' code=expr ',' level=expr ',' text=expr ')'                                                     #advisoryExpr 
      | atom                                                                                                                      #atomExpr 
      ; 

atom  : DECIMAL | BOOL | STR; 

DECIMAL: '-'? DIGIT+ ( '.' DIGIT+ )? ; 
BOOL: 'True' | 'False' ; 
STR: '\'' (ALPHANUMERIC | [ ] | '\'\'')* '\''; 
fragment DIGIT: [0-9] ; 
fragment ALPHANUMERIC: [a-z0-9A-Z!.:@#$%&^*'+/?_`~-]; 
WS : [ \t\r\n\f]+ -> skip; // Ignore/skip whitespace 