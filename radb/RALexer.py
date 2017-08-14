# Generated from RALexer.g4 by ANTLR 4.7
from antlr4 import *
from io import StringIO
from typing.io import TextIO
import sys


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2\64")
        buf.write("\u0200\b\1\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6")
        buf.write("\4\7\t\7\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r")
        buf.write("\t\r\4\16\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22")
        buf.write("\4\23\t\23\4\24\t\24\4\25\t\25\4\26\t\26\4\27\t\27\4\30")
        buf.write("\t\30\4\31\t\31\4\32\t\32\4\33\t\33\4\34\t\34\4\35\t\35")
        buf.write("\4\36\t\36\4\37\t\37\4 \t \4!\t!\4\"\t\"\4#\t#\4$\t$\4")
        buf.write("%\t%\4&\t&\4\'\t\'\4(\t(\4)\t)\4*\t*\4+\t+\4,\t,\4-\t")
        buf.write("-\4.\t.\4/\t/\4\60\t\60\4\61\t\61\4\62\t\62\4\63\t\63")
        buf.write("\4\64\t\64\4\65\t\65\4\66\t\66\4\67\t\67\48\t8\49\t9\4")
        buf.write(":\t:\4;\t;\4<\t<\4=\t=\4>\t>\4?\t?\4@\t@\4A\tA\4B\tB\4")
        buf.write("C\tC\4D\tD\4E\tE\4F\tF\4G\tG\4H\tH\4I\tI\4J\tJ\4K\tK\4")
        buf.write("L\tL\4M\tM\4N\tN\3\2\6\2\u00a0\n\2\r\2\16\2\u00a1\3\2")
        buf.write("\3\2\3\3\3\3\3\3\3\3\3\3\7\3\u00ab\n\3\f\3\16\3\u00ae")
        buf.write("\13\3\3\3\3\3\3\3\3\3\3\3\3\4\3\4\3\4\3\4\7\4\u00b9\n")
        buf.write("\4\f\4\16\4\u00bc\13\4\3\4\3\4\3\4\3\4\3\5\3\5\3\6\3\6")
        buf.write("\3\7\3\7\3\7\3\7\3\b\3\b\3\b\3\b\3\b\3\b\3\t\3\t\3\t\3")
        buf.write("\n\3\n\3\n\3\n\3\n\3\13\3\13\3\13\3\13\3\13\3\f\3\f\3")
        buf.write("\f\3\f\3\r\3\r\3\r\3\16\3\16\3\16\3\16\3\17\3\17\3\17")
        buf.write("\3\17\3\17\5\17\u00ed\n\17\3\17\7\17\u00f0\n\17\f\17\16")
        buf.write("\17\u00f3\13\17\3\17\3\17\3\20\7\20\u00f8\n\20\f\20\16")
        buf.write("\20\u00fb\13\20\3\20\5\20\u00fe\n\20\3\20\6\20\u0101\n")
        buf.write("\20\r\20\16\20\u0102\3\21\3\21\7\21\u0107\n\21\f\21\16")
        buf.write("\21\u010a\13\21\3\22\3\22\3\22\3\22\3\22\3\22\3\22\3\22")
        buf.write("\3\23\3\23\3\23\3\23\3\23\3\23\3\23\3\23\3\23\3\24\3\24")
        buf.write("\3\24\3\24\3\24\3\24\3\24\3\24\3\25\3\25\3\25\3\25\3\25")
        buf.write("\3\25\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\27\3\27\3\27")
        buf.write("\3\27\3\27\3\27\3\27\3\30\3\30\3\30\3\30\3\30\3\30\3\31")
        buf.write("\3\31\3\31\3\31\3\31\3\31\3\31\3\31\3\31\3\31\3\31\3\32")
        buf.write("\3\32\3\33\3\33\3\34\3\34\3\35\3\35\3\36\3\36\3\37\3\37")
        buf.write("\3 \3 \3 \3!\3!\3\"\3\"\3#\3#\3#\3$\3$\3%\3%\3%\3&\3&")
        buf.write("\3\'\3\'\3\'\3(\3(\3(\3)\3)\3)\3*\3*\3+\3+\3,\3,\3-\3")
        buf.write("-\3-\3-\3-\3-\3.\3.\3.\3.\3.\3.\3.\3/\3/\3/\3/\3/\3/\3")
        buf.write("\60\3\60\3\60\3\60\3\60\3\60\3\60\3\60\3\61\3\61\3\61")
        buf.write("\3\61\3\61\3\61\3\62\3\62\3\62\3\62\3\62\3\62\3\62\3\62")
        buf.write("\3\62\3\62\3\62\3\63\3\63\3\64\3\64\3\65\3\65\3\66\3\66")
        buf.write("\3\67\3\67\38\38\39\39\3:\3:\3;\3;\3<\3<\3=\3=\3>\3>\3")
        buf.write("?\3?\3@\3@\3A\3A\3B\3B\3C\3C\3D\3D\3E\3E\3F\3F\3G\3G\3")
        buf.write("H\3H\3I\3I\3J\3J\3K\3K\3L\3L\3M\6M\u01d7\nM\rM\16M\u01d8")
        buf.write("\3N\5N\u01dc\nN\3N\3N\3N\3N\5N\u01e2\nN\3N\7N\u01e5\n")
        buf.write("N\fN\16N\u01e8\13N\3N\3N\3N\3N\5N\u01ee\nN\3N\7N\u01f1")
        buf.write("\nN\fN\16N\u01f4\13N\3N\3N\7N\u01f8\nN\fN\16N\u01fb\13")
        buf.write("N\3N\3N\3N\3N\5\u00ac\u00ba\u01f9\2O\4\3\6\4\b\5\n\6\f")
        buf.write("\7\16\b\20\t\22\n\24\13\26\f\30\r\32\16\34\17\36\20 \21")
        buf.write("\"\22$\23&\24(\25*\26,\27.\30\60\31\62\32\64\33\66\34")
        buf.write("8\35:\36<\37> @!B\"D#F$H%J&L\'N(P)R*T+V,X-Z.\\/^\60`\61")
        buf.write("b\62d\63f\2h\2j\2l\2n\2p\2r\2t\2v\2x\2z\2|\2~\2\u0080")
        buf.write("\2\u0082\2\u0084\2\u0086\2\u0088\2\u008a\2\u008c\2\u008e")
        buf.write("\2\u0090\2\u0092\2\u0094\2\u0096\2\u0098\2\u009a\2\u009c")
        buf.write("\64\4\2\3\"\5\2\13\f\17\17\"\"\5\2\f\f\17\17))\5\2C\\")
        buf.write("aac|\6\2\62;C\\aac|\4\2CCcc\4\2DDdd\4\2EEee\4\2FFff\4")
        buf.write("\2GGgg\4\2HHhh\4\2IIii\4\2JJjj\4\2KKkk\4\2LLll\4\2MMm")
        buf.write("m\4\2NNnn\4\2OOoo\4\2PPpp\4\2QQqq\4\2RRrr\4\2SSss\4\2")
        buf.write("TTtt\4\2UUuu\4\2VVvv\4\2WWww\4\2XXxx\4\2YYyy\4\2ZZzz\4")
        buf.write("\2[[{{\4\2\\\\||\5\2\f\f\17\17$$\4\2$$))\2\u01fa\2\4\3")
        buf.write("\2\2\2\2\6\3\2\2\2\2\b\3\2\2\2\2\n\3\2\2\2\2\f\3\2\2\2")
        buf.write("\2\16\3\2\2\2\2\20\3\2\2\2\2\22\3\2\2\2\2\24\3\2\2\2\2")
        buf.write("\26\3\2\2\2\2\30\3\2\2\2\2\32\3\2\2\2\2\34\3\2\2\2\2\36")
        buf.write("\3\2\2\2\2 \3\2\2\2\2\"\3\2\2\2\2$\3\2\2\2\2&\3\2\2\2")
        buf.write("\2(\3\2\2\2\2*\3\2\2\2\2,\3\2\2\2\2.\3\2\2\2\2\60\3\2")
        buf.write("\2\2\2\62\3\2\2\2\2\64\3\2\2\2\2\66\3\2\2\2\28\3\2\2\2")
        buf.write("\2:\3\2\2\2\2<\3\2\2\2\2>\3\2\2\2\2@\3\2\2\2\2B\3\2\2")
        buf.write("\2\2D\3\2\2\2\2F\3\2\2\2\2H\3\2\2\2\2J\3\2\2\2\2L\3\2")
        buf.write("\2\2\2N\3\2\2\2\2P\3\2\2\2\2R\3\2\2\2\2T\3\2\2\2\2V\3")
        buf.write("\2\2\2\2X\3\2\2\2\2Z\3\2\2\2\2\\\3\2\2\2\2^\3\2\2\2\2")
        buf.write("`\3\2\2\2\2b\3\2\2\2\2d\3\2\2\2\3\u009c\3\2\2\2\4\u009f")
        buf.write("\3\2\2\2\6\u00a5\3\2\2\2\b\u00b4\3\2\2\2\n\u00c1\3\2\2")
        buf.write("\2\f\u00c3\3\2\2\2\16\u00c5\3\2\2\2\20\u00c9\3\2\2\2\22")
        buf.write("\u00cf\3\2\2\2\24\u00d2\3\2\2\2\26\u00d7\3\2\2\2\30\u00dc")
        buf.write("\3\2\2\2\32\u00e0\3\2\2\2\34\u00e3\3\2\2\2\36\u00e7\3")
        buf.write("\2\2\2 \u00f9\3\2\2\2\"\u0104\3\2\2\2$\u010b\3\2\2\2&")
        buf.write("\u0113\3\2\2\2(\u011c\3\2\2\2*\u0124\3\2\2\2,\u012a\3")
        buf.write("\2\2\2.\u0131\3\2\2\2\60\u0138\3\2\2\2\62\u013e\3\2\2")
        buf.write("\2\64\u0149\3\2\2\2\66\u014b\3\2\2\28\u014d\3\2\2\2:\u014f")
        buf.write("\3\2\2\2<\u0151\3\2\2\2>\u0153\3\2\2\2@\u0155\3\2\2\2")
        buf.write("B\u0158\3\2\2\2D\u015a\3\2\2\2F\u015c\3\2\2\2H\u015f\3")
        buf.write("\2\2\2J\u0161\3\2\2\2L\u0164\3\2\2\2N\u0166\3\2\2\2P\u0169")
        buf.write("\3\2\2\2R\u016c\3\2\2\2T\u016f\3\2\2\2V\u0171\3\2\2\2")
        buf.write("X\u0173\3\2\2\2Z\u0175\3\2\2\2\\\u017b\3\2\2\2^\u0182")
        buf.write("\3\2\2\2`\u0188\3\2\2\2b\u0190\3\2\2\2d\u0196\3\2\2\2")
        buf.write("f\u01a1\3\2\2\2h\u01a3\3\2\2\2j\u01a5\3\2\2\2l\u01a7\3")
        buf.write("\2\2\2n\u01a9\3\2\2\2p\u01ab\3\2\2\2r\u01ad\3\2\2\2t\u01af")
        buf.write("\3\2\2\2v\u01b1\3\2\2\2x\u01b3\3\2\2\2z\u01b5\3\2\2\2")
        buf.write("|\u01b7\3\2\2\2~\u01b9\3\2\2\2\u0080\u01bb\3\2\2\2\u0082")
        buf.write("\u01bd\3\2\2\2\u0084\u01bf\3\2\2\2\u0086\u01c1\3\2\2\2")
        buf.write("\u0088\u01c3\3\2\2\2\u008a\u01c5\3\2\2\2\u008c\u01c7\3")
        buf.write("\2\2\2\u008e\u01c9\3\2\2\2\u0090\u01cb\3\2\2\2\u0092\u01cd")
        buf.write("\3\2\2\2\u0094\u01cf\3\2\2\2\u0096\u01d1\3\2\2\2\u0098")
        buf.write("\u01d3\3\2\2\2\u009a\u01d6\3\2\2\2\u009c\u01db\3\2\2\2")
        buf.write("\u009e\u00a0\t\2\2\2\u009f\u009e\3\2\2\2\u00a0\u00a1\3")
        buf.write("\2\2\2\u00a1\u009f\3\2\2\2\u00a1\u00a2\3\2\2\2\u00a2\u00a3")
        buf.write("\3\2\2\2\u00a3\u00a4\b\2\2\2\u00a4\5\3\2\2\2\u00a5\u00a6")
        buf.write("\7\61\2\2\u00a6\u00a7\7,\2\2\u00a7\u00ac\3\2\2\2\u00a8")
        buf.write("\u00ab\5\6\3\2\u00a9\u00ab\13\2\2\2\u00aa\u00a8\3\2\2")
        buf.write("\2\u00aa\u00a9\3\2\2\2\u00ab\u00ae\3\2\2\2\u00ac\u00ad")
        buf.write("\3\2\2\2\u00ac\u00aa\3\2\2\2\u00ad\u00af\3\2\2\2\u00ae")
        buf.write("\u00ac\3\2\2\2\u00af\u00b0\7,\2\2\u00b0\u00b1\7\61\2\2")
        buf.write("\u00b1\u00b2\3\2\2\2\u00b2\u00b3\b\3\2\2\u00b3\7\3\2\2")
        buf.write("\2\u00b4\u00b5\7\61\2\2\u00b5\u00b6\7\61\2\2\u00b6\u00ba")
        buf.write("\3\2\2\2\u00b7\u00b9\13\2\2\2\u00b8\u00b7\3\2\2\2\u00b9")
        buf.write("\u00bc\3\2\2\2\u00ba\u00bb\3\2\2\2\u00ba\u00b8\3\2\2\2")
        buf.write("\u00bb\u00bd\3\2\2\2\u00bc\u00ba\3\2\2\2\u00bd\u00be\7")
        buf.write("\f\2\2\u00be\u00bf\3\2\2\2\u00bf\u00c0\b\4\2\2\u00c0\t")
        buf.write("\3\2\2\2\u00c1\u00c2\7=\2\2\u00c2\13\3\2\2\2\u00c3\u00c4")
        buf.write("\7#\2\2\u00c4\r\3\2\2\2\u00c5\u00c6\5\22\t\2\u00c6\u00c7")
        buf.write("\5\4\2\2\u00c7\u00c8\5\24\n\2\u00c8\17\3\2\2\2\u00c9\u00ca")
        buf.write("\5\22\t\2\u00ca\u00cb\5\4\2\2\u00cb\u00cc\5\34\16\2\u00cc")
        buf.write("\u00cd\5\4\2\2\u00cd\u00ce\5\24\n\2\u00ce\21\3\2\2\2\u00cf")
        buf.write("\u00d0\5v;\2\u00d0\u00d1\5\u008aE\2\u00d1\23\3\2\2\2\u00d2")
        buf.write("\u00d3\5\u0080@\2\u00d3\u00d4\5\u008eG\2\u00d4\u00d5\5")
        buf.write("|>\2\u00d5\u00d6\5|>\2\u00d6\25\3\2\2\2\u00d7\u00d8\5")
        buf.write("|>\2\u00d8\u00d9\5v;\2\u00d9\u00da\5z=\2\u00da\u00db\5")
        buf.write("n\67\2\u00db\27\3\2\2\2\u00dc\u00dd\5f\63\2\u00dd\u00de")
        buf.write("\5\u0080@\2\u00de\u00df\5l\66\2\u00df\31\3\2\2\2\u00e0")
        buf.write("\u00e1\5\u0082A\2\u00e1\u00e2\5\u0088D\2\u00e2\33\3\2")
        buf.write("\2\2\u00e3\u00e4\5\u0080@\2\u00e4\u00e5\5\u0082A\2\u00e5")
        buf.write("\u00e6\5\u008cF\2\u00e6\35\3\2\2\2\u00e7\u00f1\7)\2\2")
        buf.write("\u00e8\u00f0\n\3\2\2\u00e9\u00ea\7)\2\2\u00ea\u00f0\7")
        buf.write(")\2\2\u00eb\u00ed\7\17\2\2\u00ec\u00eb\3\2\2\2\u00ec\u00ed")
        buf.write("\3\2\2\2\u00ed\u00ee\3\2\2\2\u00ee\u00f0\7\f\2\2\u00ef")
        buf.write("\u00e8\3\2\2\2\u00ef\u00e9\3\2\2\2\u00ef\u00ec\3\2\2\2")
        buf.write("\u00f0\u00f3\3\2\2\2\u00f1\u00ef\3\2\2\2\u00f1\u00f2\3")
        buf.write("\2\2\2\u00f2\u00f4\3\2\2\2\u00f3\u00f1\3\2\2\2\u00f4\u00f5")
        buf.write("\7)\2\2\u00f5\37\3\2\2\2\u00f6\u00f8\5\u009aM\2\u00f7")
        buf.write("\u00f6\3\2\2\2\u00f8\u00fb\3\2\2\2\u00f9\u00f7\3\2\2\2")
        buf.write("\u00f9\u00fa\3\2\2\2\u00fa\u00fd\3\2\2\2\u00fb\u00f9\3")
        buf.write("\2\2\2\u00fc\u00fe\7\60\2\2\u00fd\u00fc\3\2\2\2\u00fd")
        buf.write("\u00fe\3\2\2\2\u00fe\u0100\3\2\2\2\u00ff\u0101\5\u009a")
        buf.write("M\2\u0100\u00ff\3\2\2\2\u0101\u0102\3\2\2\2\u0102\u0100")
        buf.write("\3\2\2\2\u0102\u0103\3\2\2\2\u0103!\3\2\2\2\u0104\u0108")
        buf.write("\t\4\2\2\u0105\u0107\t\5\2\2\u0106\u0105\3\2\2\2\u0107")
        buf.write("\u010a\3\2\2\2\u0108\u0106\3\2\2\2\u0108\u0109\3\2\2\2")
        buf.write("\u0109#\3\2\2\2\u010a\u0108\3\2\2\2\u010b\u010c\7^\2\2")
        buf.write("\u010c\u010d\7t\2\2\u010d\u010e\7g\2\2\u010e\u010f\7p")
        buf.write("\2\2\u010f\u0110\7c\2\2\u0110\u0111\7o\2\2\u0111\u0112")
        buf.write("\7g\2\2\u0112%\3\2\2\2\u0113\u0114\7^\2\2\u0114\u0115")
        buf.write("\7r\2\2\u0115\u0116\7t\2\2\u0116\u0117\7q\2\2\u0117\u0118")
        buf.write("\7l\2\2\u0118\u0119\7g\2\2\u0119\u011a\7e\2\2\u011a\u011b")
        buf.write("\7v\2\2\u011b\'\3\2\2\2\u011c\u011d\7^\2\2\u011d\u011e")
        buf.write("\7u\2\2\u011e\u011f\7g\2\2\u011f\u0120\7n\2\2\u0120\u0121")
        buf.write("\7g\2\2\u0121\u0122\7e\2\2\u0122\u0123\7v\2\2\u0123)\3")
        buf.write("\2\2\2\u0124\u0125\7^\2\2\u0125\u0126\7l\2\2\u0126\u0127")
        buf.write("\7q\2\2\u0127\u0128\7k\2\2\u0128\u0129\7p\2\2\u0129+\3")
        buf.write("\2\2\2\u012a\u012b\7^\2\2\u012b\u012c\7e\2\2\u012c\u012d")
        buf.write("\7t\2\2\u012d\u012e\7q\2\2\u012e\u012f\7u\2\2\u012f\u0130")
        buf.write("\7u\2\2\u0130-\3\2\2\2\u0131\u0132\7^\2\2\u0132\u0133")
        buf.write("\7w\2\2\u0133\u0134\7p\2\2\u0134\u0135\7k\2\2\u0135\u0136")
        buf.write("\7q\2\2\u0136\u0137\7p\2\2\u0137/\3\2\2\2\u0138\u0139")
        buf.write("\7^\2\2\u0139\u013a\7f\2\2\u013a\u013b\7k\2\2\u013b\u013c")
        buf.write("\7h\2\2\u013c\u013d\7h\2\2\u013d\61\3\2\2\2\u013e\u013f")
        buf.write("\7^\2\2\u013f\u0140\7k\2\2\u0140\u0141\7p\2\2\u0141\u0142")
        buf.write("\7v\2\2\u0142\u0143\7g\2\2\u0143\u0144\7t\2\2\u0144\u0145")
        buf.write("\7u\2\2\u0145\u0146\7g\2\2\u0146\u0147\7e\2\2\u0147\u0148")
        buf.write("\7v\2\2\u0148\63\3\2\2\2\u0149\u014a\7\60\2\2\u014a\65")
        buf.write("\3\2\2\2\u014b\u014c\7.\2\2\u014c\67\3\2\2\2\u014d\u014e")
        buf.write("\7,\2\2\u014e9\3\2\2\2\u014f\u0150\7\61\2\2\u0150;\3\2")
        buf.write("\2\2\u0151\u0152\7-\2\2\u0152=\3\2\2\2\u0153\u0154\7/")
        buf.write("\2\2\u0154?\3\2\2\2\u0155\u0156\7~\2\2\u0156\u0157\7~")
        buf.write("\2\2\u0157A\3\2\2\2\u0158\u0159\7*\2\2\u0159C\3\2\2\2")
        buf.write("\u015a\u015b\7+\2\2\u015bE\3\2\2\2\u015c\u015d\7a\2\2")
        buf.write("\u015d\u015e\7}\2\2\u015eG\3\2\2\2\u015f\u0160\7\177\2")
        buf.write("\2\u0160I\3\2\2\2\u0161\u0162\7<\2\2\u0162\u0163\7/\2")
        buf.write("\2\u0163K\3\2\2\2\u0164\u0165\7<\2\2\u0165M\3\2\2\2\u0166")
        buf.write("\u0167\7>\2\2\u0167\u0168\7?\2\2\u0168O\3\2\2\2\u0169")
        buf.write("\u016a\7>\2\2\u016a\u016b\7@\2\2\u016bQ\3\2\2\2\u016c")
        buf.write("\u016d\7@\2\2\u016d\u016e\7?\2\2\u016eS\3\2\2\2\u016f")
        buf.write("\u0170\7>\2\2\u0170U\3\2\2\2\u0171\u0172\7?\2\2\u0172")
        buf.write("W\3\2\2\2\u0173\u0174\7@\2\2\u0174Y\3\2\2\2\u0175\u0176")
        buf.write("\7^\2\2\u0176\u0177\7n\2\2\u0177\u0178\7k\2\2\u0178\u0179")
        buf.write("\7u\2\2\u0179\u017a\7v\2\2\u017a[\3\2\2\2\u017b\u017c")
        buf.write("\7^\2\2\u017c\u017d\7e\2\2\u017d\u017e\7n\2\2\u017e\u017f")
        buf.write("\7g\2\2\u017f\u0180\7c\2\2\u0180\u0181\7t\2\2\u0181]\3")
        buf.write("\2\2\2\u0182\u0183\7^\2\2\u0183\u0184\7u\2\2\u0184\u0185")
        buf.write("\7c\2\2\u0185\u0186\7x\2\2\u0186\u0187\7g\2\2\u0187_\3")
        buf.write("\2\2\2\u0188\u0189\7^\2\2\u0189\u018a\7u\2\2\u018a\u018b")
        buf.write("\7q\2\2\u018b\u018c\7w\2\2\u018c\u018d\7t\2\2\u018d\u018e")
        buf.write("\7e\2\2\u018e\u018f\7g\2\2\u018fa\3\2\2\2\u0190\u0191")
        buf.write("\7^\2\2\u0191\u0192\7s\2\2\u0192\u0193\7w\2\2\u0193\u0194")
        buf.write("\7k\2\2\u0194\u0195\7v\2\2\u0195c\3\2\2\2\u0196\u0197")
        buf.write("\7^\2\2\u0197\u0198\7u\2\2\u0198\u0199\7s\2\2\u0199\u019a")
        buf.write("\7n\2\2\u019a\u019b\7g\2\2\u019b\u019c\7z\2\2\u019c\u019d")
        buf.write("\7g\2\2\u019d\u019e\7e\2\2\u019e\u019f\3\2\2\2\u019f\u01a0")
        buf.write("\b\62\3\2\u01a0e\3\2\2\2\u01a1\u01a2\t\6\2\2\u01a2g\3")
        buf.write("\2\2\2\u01a3\u01a4\t\7\2\2\u01a4i\3\2\2\2\u01a5\u01a6")
        buf.write("\t\b\2\2\u01a6k\3\2\2\2\u01a7\u01a8\t\t\2\2\u01a8m\3\2")
        buf.write("\2\2\u01a9\u01aa\t\n\2\2\u01aao\3\2\2\2\u01ab\u01ac\t")
        buf.write("\13\2\2\u01acq\3\2\2\2\u01ad\u01ae\t\f\2\2\u01aes\3\2")
        buf.write("\2\2\u01af\u01b0\t\r\2\2\u01b0u\3\2\2\2\u01b1\u01b2\t")
        buf.write("\16\2\2\u01b2w\3\2\2\2\u01b3\u01b4\t\17\2\2\u01b4y\3\2")
        buf.write("\2\2\u01b5\u01b6\t\20\2\2\u01b6{\3\2\2\2\u01b7\u01b8\t")
        buf.write("\21\2\2\u01b8}\3\2\2\2\u01b9\u01ba\t\22\2\2\u01ba\177")
        buf.write("\3\2\2\2\u01bb\u01bc\t\23\2\2\u01bc\u0081\3\2\2\2\u01bd")
        buf.write("\u01be\t\24\2\2\u01be\u0083\3\2\2\2\u01bf\u01c0\t\25\2")
        buf.write("\2\u01c0\u0085\3\2\2\2\u01c1\u01c2\t\26\2\2\u01c2\u0087")
        buf.write("\3\2\2\2\u01c3\u01c4\t\27\2\2\u01c4\u0089\3\2\2\2\u01c5")
        buf.write("\u01c6\t\30\2\2\u01c6\u008b\3\2\2\2\u01c7\u01c8\t\31\2")
        buf.write("\2\u01c8\u008d\3\2\2\2\u01c9\u01ca\t\32\2\2\u01ca\u008f")
        buf.write("\3\2\2\2\u01cb\u01cc\t\33\2\2\u01cc\u0091\3\2\2\2\u01cd")
        buf.write("\u01ce\t\34\2\2\u01ce\u0093\3\2\2\2\u01cf\u01d0\t\35\2")
        buf.write("\2\u01d0\u0095\3\2\2\2\u01d1\u01d2\t\36\2\2\u01d2\u0097")
        buf.write("\3\2\2\2\u01d3\u01d4\t\37\2\2\u01d4\u0099\3\2\2\2\u01d5")
        buf.write("\u01d7\4\62;\2\u01d6\u01d5\3\2\2\2\u01d7\u01d8\3\2\2\2")
        buf.write("\u01d8\u01d6\3\2\2\2\u01d8\u01d9\3\2\2\2\u01d9\u009b\3")
        buf.write("\2\2\2\u01da\u01dc\5\4\2\2\u01db\u01da\3\2\2\2\u01db\u01dc")
        buf.write("\3\2\2\2\u01dc\u01dd\3\2\2\2\u01dd\u01f9\5F#\2\u01de\u01e6")
        buf.write("\7)\2\2\u01df\u01e5\n\3\2\2\u01e0\u01e2\7\17\2\2\u01e1")
        buf.write("\u01e0\3\2\2\2\u01e1\u01e2\3\2\2\2\u01e2\u01e3\3\2\2\2")
        buf.write("\u01e3\u01e5\7\f\2\2\u01e4\u01df\3\2\2\2\u01e4\u01e1\3")
        buf.write("\2\2\2\u01e5\u01e8\3\2\2\2\u01e6\u01e4\3\2\2\2\u01e6\u01e7")
        buf.write("\3\2\2\2\u01e7\u01e9\3\2\2\2\u01e8\u01e6\3\2\2\2\u01e9")
        buf.write("\u01f8\7)\2\2\u01ea\u01f2\7$\2\2\u01eb\u01f1\n \2\2\u01ec")
        buf.write("\u01ee\7\17\2\2\u01ed\u01ec\3\2\2\2\u01ed\u01ee\3\2\2")
        buf.write("\2\u01ee\u01ef\3\2\2\2\u01ef\u01f1\7\f\2\2\u01f0\u01eb")
        buf.write("\3\2\2\2\u01f0\u01ed\3\2\2\2\u01f1\u01f4\3\2\2\2\u01f2")
        buf.write("\u01f0\3\2\2\2\u01f2\u01f3\3\2\2\2\u01f3\u01f5\3\2\2\2")
        buf.write("\u01f4\u01f2\3\2\2\2\u01f5\u01f8\7$\2\2\u01f6\u01f8\n")
        buf.write("!\2\2\u01f7\u01de\3\2\2\2\u01f7\u01ea\3\2\2\2\u01f7\u01f6")
        buf.write("\3\2\2\2\u01f8\u01fb\3\2\2\2\u01f9\u01fa\3\2\2\2\u01f9")
        buf.write("\u01f7\3\2\2\2\u01fa\u01fc\3\2\2\2\u01fb\u01f9\3\2\2\2")
        buf.write("\u01fc\u01fd\5H$\2\u01fd\u01fe\3\2\2\2\u01fe\u01ff\bN")
        buf.write("\4\2\u01ff\u009d\3\2\2\2\31\2\3\u00a1\u00aa\u00ac\u00ba")
        buf.write("\u00ec\u00ef\u00f1\u00f9\u00fd\u0102\u0108\u01d8\u01db")
        buf.write("\u01e1\u01e4\u01e6\u01ed\u01f0\u01f2\u01f7\u01f9\5\b\2")
        buf.write("\2\7\3\2\6\2\2")
        return buf.getvalue()


class RALexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    SQLEXEC_MODE = 1

    WS = 1
    COMMENT = 2
    LINE_COMMENT = 3
    TERMINATOR = 4
    FORCE = 5
    IS_NULL = 6
    IS_NOT_NULL = 7
    IS = 8
    NULL = 9
    LIKE = 10
    AND = 11
    OR = 12
    NOT = 13
    STRING = 14
    NUMBER = 15
    ID = 16
    RENAME = 17
    PROJECT = 18
    SELECT = 19
    JOIN = 20
    CROSS = 21
    UNION = 22
    DIFF = 23
    INTERSECT = 24
    DOT = 25
    COMMA = 26
    STAR = 27
    SLASH = 28
    PLUS = 29
    MINUS = 30
    CONCAT = 31
    PAREN_L = 32
    PAREN_R = 33
    ARG_L = 34
    ARG_R = 35
    GETS = 36
    COLON = 37
    LE = 38
    NE = 39
    GE = 40
    LT = 41
    EQ = 42
    GT = 43
    LIST = 44
    CLEAR = 45
    SAVE = 46
    SOURCE = 47
    QUIT = 48
    SQLEXEC = 49
    SQLEXEC_TEXT = 50

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE", "SQLEXEC_MODE" ]

    literalNames = [ "<INVALID>",
            "';'", "'!'", "'\\rename'", "'\\project'", "'\\select'", "'\\join'", 
            "'\\cross'", "'\\union'", "'\\diff'", "'\\intersect'", "'.'", 
            "','", "'*'", "'/'", "'+'", "'-'", "'||'", "'('", "')'", "'_{'", 
            "'}'", "':-'", "':'", "'<='", "'<>'", "'>='", "'<'", "'='", 
            "'>'", "'\\list'", "'\\clear'", "'\\save'", "'\\source'", "'\\quit'", 
            "'\\sqlexec'" ]

    symbolicNames = [ "<INVALID>",
            "WS", "COMMENT", "LINE_COMMENT", "TERMINATOR", "FORCE", "IS_NULL", 
            "IS_NOT_NULL", "IS", "NULL", "LIKE", "AND", "OR", "NOT", "STRING", 
            "NUMBER", "ID", "RENAME", "PROJECT", "SELECT", "JOIN", "CROSS", 
            "UNION", "DIFF", "INTERSECT", "DOT", "COMMA", "STAR", "SLASH", 
            "PLUS", "MINUS", "CONCAT", "PAREN_L", "PAREN_R", "ARG_L", "ARG_R", 
            "GETS", "COLON", "LE", "NE", "GE", "LT", "EQ", "GT", "LIST", 
            "CLEAR", "SAVE", "SOURCE", "QUIT", "SQLEXEC", "SQLEXEC_TEXT" ]

    ruleNames = [ "WS", "COMMENT", "LINE_COMMENT", "TERMINATOR", "FORCE", 
                  "IS_NULL", "IS_NOT_NULL", "IS", "NULL", "LIKE", "AND", 
                  "OR", "NOT", "STRING", "NUMBER", "ID", "RENAME", "PROJECT", 
                  "SELECT", "JOIN", "CROSS", "UNION", "DIFF", "INTERSECT", 
                  "DOT", "COMMA", "STAR", "SLASH", "PLUS", "MINUS", "CONCAT", 
                  "PAREN_L", "PAREN_R", "ARG_L", "ARG_R", "GETS", "COLON", 
                  "LE", "NE", "GE", "LT", "EQ", "GT", "LIST", "CLEAR", "SAVE", 
                  "SOURCE", "QUIT", "SQLEXEC", "A", "B", "C", "D", "E", 
                  "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", 
                  "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "UNSIGNED_INTEGER_FRAGMENT", 
                  "SQLEXEC_TEXT" ]

    grammarFileName = "RALexer.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.7")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


