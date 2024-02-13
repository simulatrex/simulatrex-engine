from ply import lex, yacc

tokens = ("AGENTS", "NUMBER", "LBRACE", "RBRACE", "COLON", "COMMA", "IDENTIFIER")

t_LBRACE = r"\{"
t_RBRACE = r"\}"
t_COLON = r":"
t_COMMA = r","
t_IDENTIFIER = r"[a-zA-Z_][a-zA-Z0-9_]*"


def t_NUMBER(t):
    r"\d+"
    t.value = int(t.value)
    return t


t_ignore = " \t\n"


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()


def p_agents(p):
    "agents : IDENTIFIER LBRACE agent_defs RBRACE"
    if p[1].lower() == "agents":  # Check if the IDENTIFIER is 'Agents'
        p[0] = {"agents": p[3]}
    else:
        print(f"Syntax error: Expected 'Agents', found '{p[1]}'")


def p_agent_defs(p):
    """agent_defs : agent_def agent_defs_tail
    | agent_def"""
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = [p[1]]


def p_agent_defs_tail(p):
    """agent_defs_tail : COMMA agent_def agent_defs_tail
    | COMMA agent_def
    | empty"""
    if len(p) == 4:
        p[0] = [p[2]] + p[3]
    elif len(p) == 3:
        p[0] = [p[2]]
    else:
        p[0] = []


def p_empty(p):
    "empty :"
    pass


def p_agent_def(p):
    "agent_def : IDENTIFIER COLON NUMBER"
    p[0] = {p[1]: p[3]}


def p_error(p):
    if p:
        print(
            f"Syntax error at token {p.type}: '{p.value}', line {p.lineno}, position {p.lexpos}"
        )
    else:
        print("Syntax error at EOF")


parser = yacc.yacc()


def parse_dsl(data):
    return parser.parse(data)


# Example usage
data = """
Agents {
    num: 10
    traits: 5
}
"""
print(parse_dsl(data))
