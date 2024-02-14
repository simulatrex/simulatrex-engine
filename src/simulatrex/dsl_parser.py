from simulatrex.simulation_entities import Agent, Simulation
from jinja2 import Environment
from ply import lex, yacc


tokens = (
    "AGENT",
    "ENVIRONMENT",
    "SIMULATION",
    "IDENTIFIER",
    "COLON",
    "NUMBER",
    "ACTIONS",
    "ATTRIBUTES",
    "ELEMENTS",
    "EPOCHS",
    "INTERACTIONS",
)

t_ignore = " \t\n"

t_COLON = r":"


def t_AGENT(t):
    r"Agent"
    return t


def t_ENVIRONMENT(t):
    r"Environment"
    return t


def t_SIMULATION(t):
    r"Simulation"
    return t


def t_IDENTIFIER(t):
    r"[a-zA-Z_][a-zA-Z0-9_]*"
    return t


def t_NUMBER(t):
    r"\d+"
    t.value = int(t.value)
    return t


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()


def p_start(p):
    """start : entity
    | start entity"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]


def p_entity(p):
    """entity : AGENT IDENTIFIER
    | ENVIRONMENT IDENTIFIER
    | SIMULATION IDENTIFIER"""
    if p[1] == "Agent":
        p[0] = Agent(p[2])
    elif p[1] == "Environment":
        p[0] = Environment(p[2])
    elif p[1] == "Simulation":
        p[0] = Simulation(p[2])


def p_error(p):
    if p:
        print(
            f"Syntax error at token {p.type}: '{p.value}', line {p.lineno}, position {p.lexpos}"
        )
    else:
        print("Syntax error at EOF")


parser = yacc.yacc()


# Modify the parse_dsl function to return a Simulation instance
def parse_dsl(data):
    parsed_data = parser.parse(data)
    simulation = None
    agents = []
    environment = None
    for item in parsed_data:
        if isinstance(item, Simulation):
            simulation = item
        elif isinstance(item, Agent):
            agents.append(item)
        elif isinstance(item, Environment):
            environment = item
    if simulation:
        simulation.agents = agents
        simulation.environment = environment
    return simulation
