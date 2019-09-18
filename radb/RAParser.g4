parser grammar RAParser;
options { tokenVocab=RALexer; }

valExpr : STRING                                        # stringLiteralValExpr
        | NUMBER                                        # numberLiteralValExpr
        | PAREN_L valExpr PAREN_R                       # valExprParenthesized
        | ID PAREN_L listOfValExprs? PAREN_R            # funcExpr
        | (ID DOT)? ID                                  # attrRef
        | valExpr (STAR|SLASH) valExpr                  # multDivExpr
        | valExpr (PLUS|MINUS) valExpr                  # plusMinusExpr
        | valExpr CONCAT valExpr                        # concatExpr
        | valExpr (LT|LE|EQ|NE|GE|GT) valExpr           # compareExpr
        | valExpr LIKE valExpr                          # likeExpr
        | valExpr IS_NULL                               # isNullExpr
        | valExpr IS_NOT_NULL                           # isNotNullExpr
        | NOT valExpr                                   # notExpr
        | valExpr AND valExpr                           # andExpr
        | valExpr OR valExpr                            # orExpr
        ;
listOfValExprs : valExpr (COMMA listOfValExprs)?;

listOfIDs : ID (COMMA listOfIDs)?;

relExpr  : PAREN_L relExpr PAREN_R                      # relExprParenthesized
         | ID                                           # relRef
         | RENAME ARG_L ((ID COLON (STAR|listOfIDs)) | listOfIDs) ARG_R relExpr # renameExpr
         | PROJECT ARG_L listOfValExprs ARG_R relExpr   # projectExpr
         | SELECT ARG_L valExpr ARG_R relExpr           # selectExpr
         | relExpr JOIN (ARG_L valExpr ARG_R)? relExpr  # joinExpr
         | relExpr CROSS relExpr                        # crossExpr
         | relExpr UNION relExpr                        # unionExpr
         | relExpr DIFF relExpr                         # diffExpr
         | relExpr INTERSECT relExpr                    # intersectExpr
         | AGGR ARG_L listOfValExprs (COLON listOfValExprs)? ARG_R relExpr      # aggrExpr
         ;

definition : ID GETS relExpr;

command : LIST                                          # listCommand
        | CLEAR (FORCE? ID|STAR)                        # clearCommand
        | SAVE FORCE? (ID|STAR) STRING?                 # saveCommand
        | SOURCE STRING                                 # sourceCommand
        | HELP                                          # helpCommand
        | QUIT                                          # quitCommand
        | SQLEXEC SQLEXEC_TEXT                          # sqlexecCommand
        ;

statement : (relExpr|definition|command) TERMINATOR;
program : (statement)* EOF;
