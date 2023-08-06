import json
from sly import Parser
from mindsdb_sql.parser.ast import *
from mindsdb_sql.parser.dialects.mindsdb.drop_integration import DropIntegration
from mindsdb_sql.parser.dialects.mindsdb.drop_predictor import DropPredictor
from mindsdb_sql.parser.dialects.mindsdb.create_predictor import CreatePredictor
from mindsdb_sql.parser.dialects.mindsdb.create_integration import CreateIntegration
from mindsdb_sql.parser.dialects.mindsdb.create_view import CreateView
from mindsdb_sql.parser.dialects.mindsdb.latest import Latest
from mindsdb_sql.exceptions import ParsingException
from mindsdb_sql.parser.dialects.mindsdb.lexer import MindsDBLexer
from mindsdb_sql.parser.dialects.mindsdb.retrain_predictor import RetrainPredictor
from mindsdb_sql.parser.logger import ParserLogger
from mindsdb_sql.utils import ensure_select_keyword_order, JoinType

"""
Unfortunately the rules are not iherited from base SQLParser, because it just doesn't work with Sly due to metaclass magic.
"""
class MindsDBParser(Parser):
    log = ParserLogger()
    tokens = MindsDBLexer.tokens

    precedence = (
        ('left', PLUS, MINUS, OR),
        ('left', STAR, DIVIDE, AND),
        ('right', UMINUS, UNOT),  # Unary minus operator, unary not
        ('nonassoc', LESS, LEQ, GREATER, GEQ, EQUALS, NEQUALS, IN, BETWEEN, IS, LIKE),
    )

    # Top-level statements
    @_('show',
       'start_transaction',
       'commit_transaction',
       'rollback_transaction',
       'alter_table',
       'explain',
       'set',
       'use',
       'describe',
       'create_predictor',
       'datasource_engine',
       'create_integration',
       'create_view',
       'drop_predictor',
       'retrain_predictor',
       'drop_integration',
       'union',
       'select',
       )
    def query(self, p):
        return p[0]

    # Explain
    @_('EXPLAIN identifier')
    def explain(self, p):
        return Explain(target=p.identifier)

    # Alter table
    @_('ALTER TABLE identifier ID ID')
    def alter_table(self, p):
        return AlterTable(target=p.identifier,
                          arg=' '.join([p.ID0, p.ID1]))

    # Transactions

    @_('START TRANSACTION')
    def start_transaction(self, p):
        return StartTransaction()

    @_('COMMIT')
    def commit_transaction(self, p):
        return CommitTransaction()

    @_('ROLLBACK')
    def rollback_transaction(self, p):
        return RollbackTransaction()

    # Set

    @_('SET AUTOCOMMIT')
    def set(self, p):
        return Set(category=p.AUTOCOMMIT)

    @_('SET expr')
    def set(self, p):
        return Set(arg=p.expr)

    @_('SET ID identifier')
    def set(self, p):
        if not p.ID.lower() == 'names':
            raise ParsingException(f'Expected "SET names", got "SET {p.ID}"')
        return Set(category=p.ID.lower(), arg=p.identifier)

    # Show

    @_('SHOW show_category show_condition_or_nothing')
    def show(self, p):
        condition = p.show_condition_or_nothing['condition'] if p.show_condition_or_nothing else None
        expression = p.show_condition_or_nothing['expression'] if p.show_condition_or_nothing else None
        return Show(category=p.show_category,
                    condition=condition,
                    expression=expression)

    @_('show_condition_token expr',
       'empty')
    def show_condition_or_nothing(self, p):
        if not p[0]:
            return None
        return dict(condition=p[0], expression=p[1])

    @_('WHERE',
       'FROM',
       'LIKE')
    def show_condition_token(self, p):
        return p[0]

    @_('SCHEMAS',
       'DATABASES',
       'TABLES',
       'FULL TABLES',
       'VARIABLES',
       'PLUGINS',
       'SESSION VARIABLES',
       'SESSION STATUS',
       'GLOBAL VARIABLES',
       'PROCEDURE STATUS',
       'FUNCTION STATUS',
       'INDEX',
       'CREATE TABLE',
       'WARNINGS',
       'ENGINES',
       'CHARSET',
       'CHARACTER SET',
       'COLLATION',
       'TABLE STATUS',
       'STATUS',
       # Mindsdb specific
       'VIEWS',
       'STREAMS',
       'PREDICTORS',
       'INTEGRATIONS',
       'DATASOURCES',
       'PUBLICATIONS',
       'DATASETS',
       'ALL')
    def show_category(self, p):
        return ' '.join([x for x in p])

    # DESCRIBE

    @_('DESCRIBE identifier')
    def describe(self, p):
        return Describe(value=p.identifier)

    # USE

    @_('USE identifier')
    def use(self, p):
        return Use(value=p.identifier)

    # CREATE VIEW
    @_('CREATE VIEW ID create_view_from_table_or_nothing AS LPAREN select RPAREN')
    def create_view(self, p):
        return CreateView(name=p.ID,
                          from_table=p.create_view_from_table_or_nothing,
                          query=p.select)

    @_('FROM identifier')
    def create_view_from_table_or_nothing(self, p):
        return p.identifier

    @_('empty')
    def create_view_from_table_or_nothing(self, p):
        pass

    # RETRAIN PREDICTOR
    @_('RETRAIN identifier')
    def retrain_predictor(self, p):
        return RetrainPredictor(p.identifier)

    # DROP PREDICTOR
    @_('DROP PREDICTOR identifier',
       'DROP TABLE identifier')
    def drop_predictor(self, p):
        return DropPredictor(p.identifier)

    # DROP INTEGRATION
    @_('DROP INTEGRATION identifier')
    def drop_integration(self, p):
        return DropIntegration(p.identifier)

    # CREATE PREDICTOR
    @_('create_predictor USING JSON')
    def create_predictor(self, p):
        p.create_predictor.using = p.JSON
        return p.create_predictor

    @_('create_predictor HORIZON INTEGER')
    def create_predictor(self, p):
        p.create_predictor.horizon = p.INTEGER
        return p.create_predictor

    @_('create_predictor WINDOW INTEGER')
    def create_predictor(self, p):
        p.create_predictor.window = p.INTEGER
        return p.create_predictor

    @_('create_predictor GROUP_BY expr_list')
    def create_predictor(self, p):
        group_by = p.expr_list
        if not isinstance(group_by, list):
            group_by = [group_by]

        p.create_predictor.group_by = group_by
        return p.create_predictor

    @_('create_predictor ORDER_BY ordering_terms')
    def create_predictor(self, p):
        p.create_predictor.order_by = p.ordering_terms
        return p.create_predictor

    @_('CREATE PREDICTOR identifier FROM identifier WITH STRING optional_data_source_name PREDICT result_columns')
    def create_predictor(self, p):
        return CreatePredictor(
            name=p.identifier0,
            integration_name=p.identifier1,
            query=p.STRING,
            datasource_name=p.optional_data_source_name,
            targets=p.result_columns,
        )

    @_('AS identifier')
    def optional_data_source_name(self, p):
        return p.identifier

    @_('empty')
    def optional_data_source_name(self, p):
        pass

    # CREATE INTEGRATION
    @_('CREATE datasource_engine COMMA PARAMETERS EQUALS JSON',
       'CREATE datasource_engine COMMA PARAMETERS JSON',
       'CREATE datasource_engine PARAMETERS EQUALS JSON',
       'CREATE datasource_engine PARAMETERS JSON')
    def create_integration(self, p):
        return CreateIntegration(name=p.datasource_engine['id'],
                                 engine=p.datasource_engine['engine'],
                                 parameters=p.JSON)

    @_('INTEGRATION ID WITH ENGINE EQUALS STRING',
       'INTEGRATION ID WITH ENGINE STRING',
       'DATASOURCE ID WITH ENGINE EQUALS STRING',
       'DATASOURCE ID WITH ENGINE STRING')
    def datasource_engine(self, p):
        return {'id': p.ID, 'engine': p.STRING}

    # UNION / UNION ALL
    @_('select UNION select')
    def union(self, p):
        return Union(left=p.select0, right=p.select1, unique=True)

    @_('select UNION ALL select')
    def union(self, p):
        return Union(left=p.select0, right=p.select1, unique=False)

    # WITH
    @_('ctes select')
    def select(self, p):
        select = p.select
        select.cte = p.ctes
        return select

    @_('ctes COMMA identifier cte_columns_or_nothing AS LPAREN select RPAREN')
    def ctes(self, p):
        ctes = p.ctes
        ctes = ctes + [
            CommonTableExpression(
                name=p.identifier,
                columns=p.cte_columns_or_nothing,
                query=p.select)
        ]
        return ctes

    @_('WITH identifier cte_columns_or_nothing AS LPAREN select RPAREN')
    def ctes(self, p):
        return [
            CommonTableExpression(
                name=p.identifier,
                columns=p.cte_columns_or_nothing,
                query=p.select)
        ]

    @_('empty')
    def cte_columns_or_nothing(self, p):
        pass

    @_('LPAREN enumeration RPAREN')
    def cte_columns_or_nothing(self, p):
        return p.enumeration

    # SELECT
    @_('select OFFSET constant')
    def select(self, p):
        select = p.select
        if select.offset is not None:
            raise ParsingException(f'OFFSET already specified for this query')
        ensure_select_keyword_order(select, 'OFFSET')
        if not isinstance(p.constant.value, int):
            raise ParsingException(f'OFFSET must be an integer value, got: {p.constant.value}')

        select.offset = p.constant
        return select

    @_('select LIMIT constant COMMA constant')
    def select(self, p):
        select = p.select
        ensure_select_keyword_order(select, 'LIMIT')
        if not isinstance(p.constant0.value, int) or not isinstance(p.constant1.value, int):
            raise ParsingException(f'LIMIT must have integer arguments, got: {p.constant0.value}, {p.constant1.value}')
        select.offset = p.constant0
        select.limit = p.constant1
        return select

    @_('select LIMIT constant')
    def select(self, p):
        select = p.select
        ensure_select_keyword_order(select, 'LIMIT')
        if not isinstance(p.constant.value, int):
            raise ParsingException(f'LIMIT must be an integer value, got: {p.constant.value}')
        select.limit = p.constant
        return select

    @_('select ORDER_BY ordering_terms')
    def select(self, p):
        select = p.select
        ensure_select_keyword_order(select, 'ORDER BY')
        select.order_by = p.ordering_terms
        return select

    @_('ordering_terms COMMA ordering_term')
    def ordering_terms(self, p):
        terms = p.ordering_terms
        terms.append(p.ordering_term)
        return terms

    @_('ordering_term')
    def ordering_terms(self, p):
        return [p.ordering_term]

    @_('ordering_term NULLS_FIRST')
    def ordering_term(self, p):
        p.ordering_term.nulls = p.NULLS_FIRST
        return p.ordering_term

    @_('ordering_term NULLS_LAST')
    def ordering_term(self, p):
        p.ordering_term.nulls = p.NULLS_LAST
        return p.ordering_term

    @_('identifier DESC')
    def ordering_term(self, p):
        return OrderBy(field=p.identifier, direction='DESC')

    @_('identifier ASC')
    def ordering_term(self, p):
        return OrderBy(field=p.identifier, direction='ASC')

    @_('identifier')
    def ordering_term(self, p):
        return OrderBy(field=p.identifier, direction='default')

    @_('select HAVING expr')
    def select(self, p):
        select = p.select
        ensure_select_keyword_order(select, 'HAVING')
        having = p.expr
        if not isinstance(having, Operation):
            raise ParsingException(
                f"HAVING must contain an operation that evaluates to a boolean, got: {str(having)}")
        select.having = having
        return select

    @_('select GROUP_BY expr_list')
    def select(self, p):
        select = p.select
        ensure_select_keyword_order(select, 'GROUP BY')
        group_by = p.expr_list
        if not isinstance(group_by, list):
            group_by = [group_by]

        select.group_by = group_by
        return select

    @_('select WHERE expr')
    def select(self, p):
        select = p.select
        ensure_select_keyword_order(select, 'WHERE')
        where_expr = p.expr
        if not isinstance(where_expr, Operation):
            raise ParsingException(
                f"WHERE must contain an operation that evaluates to a boolean, got: {str(where_expr)}")
        select.where = where_expr
        return select

    # Special cases for keyword-like identifiers
    @_('select FROM TABLES')
    def select(self, p):
        select = p.select
        ensure_select_keyword_order(select, 'FROM')
        select.from_table = Identifier(p.TABLES)
        return select

    @_('select FROM from_table')
    def select(self, p):
        select = p.select
        ensure_select_keyword_order(select, 'FROM')
        select.from_table = p.from_table
        return select

    @_('from_table join_clause from_table')
    def from_table(self, p):
        return Join(left=p.from_table0,
                    right=p.from_table1,
                    join_type=p.join_clause)

    @_('from_table COMMA from_table')
    def from_table(self, p):
        return Join(left=p.from_table0,
                    right=p.from_table1,
                    join_type=JoinType.INNER_JOIN,
                    implicit=True)

    @_('from_table join_clause from_table ON expr')
    def from_table(self, p):
        return Join(left=p.from_table0,
                    right=p.from_table1,
                    join_type=p.join_clause,
                    condition=p.expr)

    @_('from_table AS identifier',
       'from_table identifier')
    def from_table(self, p):
        entity = p.from_table
        entity.alias = p.identifier
        return entity

    @_('LPAREN query RPAREN')
    def from_table(self, p):
        query = p.query
        query.parentheses = True
        return query

    @_('identifier')
    def from_table(self, p):
        return p.identifier

    @_('parameter')
    def from_table(self, p):
        return p.parameter

    @_('JOIN',
       'LEFT JOIN',
       'RIGHT JOIN',
       'INNER JOIN',
       'FULL JOIN',
       'CROSS JOIN',
       'OUTER JOIN',
       )
    def join_clause(self, p):
        return ' '.join([x for x in p])

    @_('SELECT DISTINCT result_columns')
    def select(self, p):
        targets = p.result_columns
        return Select(targets=targets, distinct=True)

    @_('SELECT result_columns')
    def select(self, p):
        targets = p.result_columns
        return Select(targets=targets)

    @_('result_columns COMMA result_column')
    def result_columns(self, p):
        p.result_columns.append(p.result_column)
        return p.result_columns

    @_('result_column')
    def result_columns(self, p):
        return [p.result_column]

    @_('result_column AS identifier',
       'result_column identifier')
    def result_column(self, p):
        col = p.result_column
        if col.alias:
            raise ParsingException(f'Attempt to provide two aliases for {str(col)}')
        col.alias = p.identifier
        return col

    @_('LPAREN select RPAREN')
    def result_column(self, p):
        select = p.select
        select.parentheses = True
        return select

    @_('star')
    def result_column(self, p):
        return p.star

    @_('expr')
    def result_column(self, p):
        return p.expr

    # OPERATIONS

    @_('LPAREN select RPAREN')
    def expr(self, p):
        select = p.select
        select.parentheses = True
        return select

    @_('LPAREN expr RPAREN')
    def expr(self, p):
        if isinstance(p.expr, ASTNode):
            p.expr.parentheses = True
        return p.expr

    @_('ID LPAREN DISTINCT expr_list RPAREN')
    def expr(self, p):
        return Function(op=p.ID, distinct=True, args=p.expr_list)

    @_('ID LPAREN expr_list_or_nothing RPAREN')
    def expr(self, p):
        args = p.expr_list_or_nothing
        if not args:
            args = []
        return Function(op=p.ID, args=args)

    # arguments are optional in functions, so that things like `select database()` are possible
    @_('expr BETWEEN expr AND expr')
    def expr(self, p):
        return BetweenOperation(args=(p.expr0, p.expr1, p.expr2))

    @_('expr_list')
    def expr_list_or_nothing(self, p):
        return p.expr_list

    @_('empty')
    def expr_list_or_nothing(self, p):
        pass

    @_('CAST LPAREN expr AS ID RPAREN')
    def expr(self, p):
        return TypeCast(arg=p.expr, type_name=str(p.ID))

    @_('enumeration')
    def expr_list(self, p):
        return p.enumeration

    @_('expr')
    def expr_list(self, p):
        return [p.expr]

    @_('LPAREN enumeration RPAREN')
    def expr(self, p):
        tup = Tuple(items=p.enumeration)
        return tup

    @_('STAR')
    def star(self, p):
        return Star()

    @_('expr IS NOT expr',
       'expr NOT IN expr')
    def expr(self, p):
        op = p[1] + ' ' + p[2]
        return BinaryOperation(op=op, args=(p.expr0, p.expr1))

    @_('expr PLUS expr',
       'expr MINUS expr',
       'expr STAR expr',
       'expr DIVIDE expr',
       'expr MODULO expr',
       'expr EQUALS expr',
       'expr NEQUALS expr',
       'expr GEQ expr',
       'expr GREATER expr',
       'expr LEQ expr',
       'expr LESS expr',
       'expr AND expr',
       'expr OR expr',
       'expr NOT expr',
       'expr IS expr',
       'expr LIKE expr',
       'expr CONCAT expr',
       'expr IN expr')
    def expr(self, p):
        return BinaryOperation(op=p[1], args=(p.expr0, p.expr1))


    @_('MINUS expr %prec UMINUS',
       'NOT expr %prec UNOT', )
    def expr(self, p):
        return UnaryOperation(op=p[0], args=(p.expr,))

    # EXPRESSIONS

    @_('enumeration COMMA expr')
    def enumeration(self, p):
        return p.enumeration + [p.expr]

    @_('expr COMMA expr')
    def enumeration(self, p):
        return [p.expr0, p.expr1]

    @_('identifier')
    def expr(self, p):
        return p.identifier

    @_('parameter')
    def expr(self, p):
        return p.parameter

    @_('constant')
    def expr(self, p):
        return p.constant

    @_('latest')
    def expr(self, p):
        return p.latest

    @_('LATEST')
    def latest(self, p):
        return Latest()

    @_('NULL')
    def constant(self, p):
        return NullConstant()

    @_('TRUE')
    def constant(self, p):
        return Constant(value=True)

    @_('FALSE')
    def constant(self, p):
        return Constant(value=False)

    @_('INTEGER')
    def constant(self, p):
        return Constant(value=int(p.INTEGER))

    @_('FLOAT')
    def constant(self, p):
        return Constant(value=float(p.FLOAT))

    @_('STRING')
    def constant(self, p):
        return Constant(value=str(p.STRING))

    @_('identifier DOT identifier')
    def identifier(self, p):
        p.identifier0.parts += p.identifier1.parts
        return p.identifier0

    @_('ID',
       'CHARSET',
       'TABLES',
       # Mindsdb specific
       'STATUS',
       'PREDICT',
       'PREDICTOR',
       'PREDICTORS')
    def identifier(self, p):
        value = p[0]
        return Identifier.from_path_str(value)

    @_('PARAMETER')
    def parameter(self, p):
        return Parameter(value=p.PARAMETER)

    @_('')
    def empty(self, p):
        pass

    def error(self, p):
        if p:
            raise ParsingException(f"Syntax error at token {p.type}: \"{p.value}\"")
        else:
            raise ParsingException("Syntax error at EOF")
