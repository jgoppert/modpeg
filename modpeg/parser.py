from parsimonious.grammar import Grammar

modelica_parser = Grammar(r"""
    #===============================================================
    # STORED DEFINITION
    #===============================================================
    stored_definition = _ (within name? semicolon)?
        (final? class_definition semicolon)*

    #===============================================================
    # CLASS DEFINITION
    #===============================================================
    class_definition = encapsulated? class_prefixes class_specifier

    class_prefixes = partial?
        (class/model/record/block/expandable/
        connector/type/package/function/operator/
        (function/record)?)

    class_specifier = long_class_specifier/
        short_class_specifier/der_class_specifier

    long_class_specifier = ident string_comment?
        composition end ident

    short_class_specifier = (ident equals base_prefix name
        array_subscripts? class_modification? comment) /
        (ident  equals enumeration lparen (enum_list/colon) rparen comment)

    der_class_specifier = ident equals der lparen name comma
        ident (comma ident )* rparen comment

    base_prefix = type_prefix

    enum_list = enumeration_literal (comma enumeration_literal)*

    enumeration_literal = ident comment

    composition = element_list (((public/protected)
       element_list)/ equation_section/ algorithm_section)*
       (external language_specification?
       external_function_call? annotation? semicolon)?

    language_specification = string

    external_function_call = (component_reference equals) ident
        lparen expression_list? rparen

    element_list = (element semicolon)*

    element = import_clause/ extends_clause

    import_clause = ''

    #===============================================================
    # EXTENDS
    #===============================================================
    extends_clause = ''

    constraining_clause = ''

    #===============================================================
    # COMPONENT CLAUSE
    #===============================================================
    component_clause = ''

    type_prefix = ''

    type_specifier = ''

    component_list = ''

    component_declaration = ''

    condition_attribute = ''

    declaration = ''

    #===============================================================
    # MODIFICATION
    #===============================================================
    modification = ''

    class_modification = ''

    argument_list = ''

    argument = ''

    element_modification_or_replacement = ''

    element_modification = ''

    element_redeclaratioin = ''

    element_replaceable = ''

    component_clause1 = ''

    component_declaration1 = ''

    short_class_definition = ''

    #===============================================================
    # EQUATION
    #===============================================================
    equation_section = ''

    algorithm_section = ''

    equation = ''

    statement = ''

    if_equation = ''

    if_statement = ''

    for_equation = ''

    for_statement = ''

    for_indices = ''

    for_index = ''

    when_statement = ''

    when_equation = ''

    when_statement = ''

    connect_clause = ''

    # EXPRESSION
    expression = ''

    simple_expression = ''

    logical_expression = ''

    logical_term = ''

    logical_factor = ''

    relation = ''

    rel_op = ''

    arithmetic_expression = ''

    add_op = ''

    term = ''

    mul_op = ''

    factor = ''

    primary = ''

    name = '.'? _ ident ('.' _ ident)*

    component_reference = ''

    function_call_args = ''

    function_arguments = ''

    named_arguments = ''

    named_argument = ''

    function_argument = ''

    output_expression_list = ''

    expression_list = ''

    array_subscripts = ''

    subscript = ''

    comment = string_comment annotation?_

    string_comment=~r'".*"'_

    annotation = ''_

    #===============================================================
    # KEYWORDS
    #===============================================================
    algorithm = 'algorithm'_
    block = 'block'_
    break = 'break'_
    class = 'class'_
    connector = 'connector'_
    constant = 'constant'_
    constrainedby = 'constrainedby'_
    der = 'der'_
    discrete = 'discrete'_
    each = 'each'_
    else = 'else'_
    elseif = 'elseif'_
    encapsulated = 'encapsulated'_
    end = 'end'_
    enumeration = 'enumeration'_
    equation = 'equation'_
    expandable = 'expandable'_
    extends = 'extends'_
    external = 'external'_
    final = 'final'_
    flow = 'flow'_
    function = 'function'_
    for= 'for'_
    if = 'if'_
    import = 'import'_
    inner = 'inner'_
    input = 'input'_
    initial = 'initial'_
    loop = 'loop'_
    model = 'model'_
    public = 'public'_
    protected = 'protected'_
    partial = 'partial'_
    parameter = 'parameter'_
    record = 'record'_
    replaceable = 'replaceable'_
    type = 'type'_
    operator = 'operator'_
    output = 'output'_
    package = 'package'_
    record = 'record'_
    redeclare = 'redeclare'_
    replaceable = 'replaceable'_
    return = 'return'_
    then = 'then'_
    outer = 'outer'_
    stream = 'stream'_
    within = 'within'_
    while = 'while'_

    #===============================================================
    # BASIC
    #===============================================================
    _ = ~r'\s*'
    ident = ~r'[A-Za-z]+'_
    string = ~r'[A-Za-z]+'_
    equals = '='_
    semicolon = ';'_
    lparen = '('_
    rparen = ')'_
    colon = ':'_
    comma = ','_
    """)
