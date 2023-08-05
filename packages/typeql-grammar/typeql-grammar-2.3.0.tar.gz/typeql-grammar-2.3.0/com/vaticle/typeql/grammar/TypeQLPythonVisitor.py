# Generated from /home/grabl/.cache/bazel/_bazel_grabl/7ef8d994fdedbcf15566d4e42e182314/sandbox/linux-sandbox/32/execroot/vaticle_typeql/bazel-out/k8-fastbuild/bin/grammar/TypeQLPython.g4 by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .TypeQLPythonParser import TypeQLPythonParser
else:
    from TypeQLPythonParser import TypeQLPythonParser

# This class defines a complete generic visitor for a parse tree produced by TypeQLPythonParser.

class TypeQLPythonVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by TypeQLPythonParser#eof_query.
    def visitEof_query(self, ctx:TypeQLPythonParser.Eof_queryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeQLPythonParser#eof_queries.
    def visitEof_queries(self, ctx:TypeQLPythonParser.Eof_queriesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeQLPythonParser#eof_pattern.
    def visitEof_pattern(self, ctx:TypeQLPythonParser.Eof_patternContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeQLPythonParser#eof_patterns.
    def visitEof_patterns(self, ctx:TypeQLPythonParser.Eof_patternsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeQLPythonParser#eof_definables.
    def visitEof_definables(self, ctx:TypeQLPythonParser.Eof_definablesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeQLPythonParser#eof_variable.
    def visitEof_variable(self, ctx:TypeQLPythonParser.Eof_variableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeQLPythonParser#eof_label.
    def visitEof_label(self, ctx:TypeQLPythonParser.Eof_labelContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeQLPythonParser#eof_schema_rule.
    def visitEof_schema_rule(self, ctx:TypeQLPythonParser.Eof_schema_ruleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeQLPythonParser#query.
    def visitQuery(self, ctx:TypeQLPythonParser.QueryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeQLPythonParser#query_define.
    def visitQuery_define(self, ctx:TypeQLPythonParser.Query_defineContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeQLPythonParser#query_undefine.
    def visitQuery_undefine(self, ctx:TypeQLPythonParser.Query_undefineContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeQLPythonParser#query_insert.
    def visitQuery_insert(self, ctx:TypeQLPythonParser.Query_insertContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeQLPythonParser#query_delete_or_update.
    def visitQuery_delete_or_update(self, ctx:TypeQLPythonParser.Query_delete_or_updateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeQLPythonParser#query_match.
    def visitQuery_match(self, ctx:TypeQLPythonParser.Query_matchContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeQLPythonParser#query_compute.
    def visitQuery_compute(self, ctx:TypeQLPythonParser.Query_computeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeQLPythonParser#query_match_aggregate.
    def visitQuery_match_aggregate(self, ctx:TypeQLPythonParser.Query_match_aggregateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeQLPythonParser#query_match_group.
    def visitQuery_match_group(self, ctx:TypeQLPythonParser.Query_match_groupContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeQLPythonParser#query_match_group_agg.
    def visitQuery_match_group_agg(self, ctx:TypeQLPythonParser.Query_match_group_aggContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeQLPythonParser#modifiers.
    def visitModifiers(self, ctx:TypeQLPythonParser.ModifiersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeQLPythonParser#filter_.
    def visitFilter_(self, ctx:TypeQLPythonParser.Filter_Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeQLPythonParser#sort.
    def visitSort(self, ctx:TypeQLPythonParser.SortContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeQLPythonParser#offset.
    def visitOffset(self, ctx:TypeQLPythonParser.OffsetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeQLPythonParser#limit.
    def visitLimit(self, ctx:TypeQLPythonParser.LimitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeQLPythonParser#match_aggregate.
    def visitMatch_aggregate(self, ctx:TypeQLPythonParser.Match_aggregateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeQLPythonParser#aggregate_method.
    def visitAggregate_method(self, ctx:TypeQLPythonParser.Aggregate_methodContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeQLPythonParser#match_group.
    def visitMatch_group(self, ctx:TypeQLPythonParser.Match_groupContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeQLPythonParser#definables.
    def visitDefinables(self, ctx:TypeQLPythonParser.DefinablesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeQLPythonParser#definable.
    def visitDefinable(self, ctx:TypeQLPythonParser.DefinableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeQLPythonParser#patterns.
    def visitPatterns(self, ctx:TypeQLPythonParser.PatternsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeQLPythonParser#pattern.
    def visitPattern(self, ctx:TypeQLPythonParser.PatternContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeQLPythonParser#pattern_conjunction.
    def visitPattern_conjunction(self, ctx:TypeQLPythonParser.Pattern_conjunctionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeQLPythonParser#pattern_disjunction.
    def visitPattern_disjunction(self, ctx:TypeQLPythonParser.Pattern_disjunctionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeQLPythonParser#pattern_negation.
    def visitPattern_negation(self, ctx:TypeQLPythonParser.Pattern_negationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeQLPythonParser#pattern_variable.
    def visitPattern_variable(self, ctx:TypeQLPythonParser.Pattern_variableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeQLPythonParser#variable_concept.
    def visitVariable_concept(self, ctx:TypeQLPythonParser.Variable_conceptContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeQLPythonParser#variable_type.
    def visitVariable_type(self, ctx:TypeQLPythonParser.Variable_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeQLPythonParser#type_constraint.
    def visitType_constraint(self, ctx:TypeQLPythonParser.Type_constraintContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeQLPythonParser#variable_things.
    def visitVariable_things(self, ctx:TypeQLPythonParser.Variable_thingsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeQLPythonParser#variable_thing_any.
    def visitVariable_thing_any(self, ctx:TypeQLPythonParser.Variable_thing_anyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeQLPythonParser#variable_thing.
    def visitVariable_thing(self, ctx:TypeQLPythonParser.Variable_thingContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeQLPythonParser#variable_relation.
    def visitVariable_relation(self, ctx:TypeQLPythonParser.Variable_relationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeQLPythonParser#variable_attribute.
    def visitVariable_attribute(self, ctx:TypeQLPythonParser.Variable_attributeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeQLPythonParser#relation.
    def visitRelation(self, ctx:TypeQLPythonParser.RelationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeQLPythonParser#role_player.
    def visitRole_player(self, ctx:TypeQLPythonParser.Role_playerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeQLPythonParser#player.
    def visitPlayer(self, ctx:TypeQLPythonParser.PlayerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeQLPythonParser#attributes.
    def visitAttributes(self, ctx:TypeQLPythonParser.AttributesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeQLPythonParser#attribute.
    def visitAttribute(self, ctx:TypeQLPythonParser.AttributeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeQLPythonParser#predicate.
    def visitPredicate(self, ctx:TypeQLPythonParser.PredicateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeQLPythonParser#predicate_equality.
    def visitPredicate_equality(self, ctx:TypeQLPythonParser.Predicate_equalityContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeQLPythonParser#predicate_substring.
    def visitPredicate_substring(self, ctx:TypeQLPythonParser.Predicate_substringContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeQLPythonParser#predicate_value.
    def visitPredicate_value(self, ctx:TypeQLPythonParser.Predicate_valueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeQLPythonParser#schema_rule.
    def visitSchema_rule(self, ctx:TypeQLPythonParser.Schema_ruleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeQLPythonParser#compute_conditions.
    def visitCompute_conditions(self, ctx:TypeQLPythonParser.Compute_conditionsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeQLPythonParser#compute_method.
    def visitCompute_method(self, ctx:TypeQLPythonParser.Compute_methodContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeQLPythonParser#conditions_count.
    def visitConditions_count(self, ctx:TypeQLPythonParser.Conditions_countContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeQLPythonParser#conditions_value.
    def visitConditions_value(self, ctx:TypeQLPythonParser.Conditions_valueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeQLPythonParser#conditions_central.
    def visitConditions_central(self, ctx:TypeQLPythonParser.Conditions_centralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeQLPythonParser#conditions_cluster.
    def visitConditions_cluster(self, ctx:TypeQLPythonParser.Conditions_clusterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeQLPythonParser#conditions_path.
    def visitConditions_path(self, ctx:TypeQLPythonParser.Conditions_pathContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeQLPythonParser#input_count.
    def visitInput_count(self, ctx:TypeQLPythonParser.Input_countContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeQLPythonParser#input_value.
    def visitInput_value(self, ctx:TypeQLPythonParser.Input_valueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeQLPythonParser#input_central.
    def visitInput_central(self, ctx:TypeQLPythonParser.Input_centralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeQLPythonParser#input_cluster.
    def visitInput_cluster(self, ctx:TypeQLPythonParser.Input_clusterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeQLPythonParser#input_path.
    def visitInput_path(self, ctx:TypeQLPythonParser.Input_pathContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeQLPythonParser#compute_direction.
    def visitCompute_direction(self, ctx:TypeQLPythonParser.Compute_directionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeQLPythonParser#compute_target.
    def visitCompute_target(self, ctx:TypeQLPythonParser.Compute_targetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeQLPythonParser#compute_scope.
    def visitCompute_scope(self, ctx:TypeQLPythonParser.Compute_scopeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeQLPythonParser#compute_config.
    def visitCompute_config(self, ctx:TypeQLPythonParser.Compute_configContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeQLPythonParser#compute_algorithm.
    def visitCompute_algorithm(self, ctx:TypeQLPythonParser.Compute_algorithmContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeQLPythonParser#compute_args.
    def visitCompute_args(self, ctx:TypeQLPythonParser.Compute_argsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeQLPythonParser#compute_args_array.
    def visitCompute_args_array(self, ctx:TypeQLPythonParser.Compute_args_arrayContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeQLPythonParser#compute_arg.
    def visitCompute_arg(self, ctx:TypeQLPythonParser.Compute_argContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeQLPythonParser#type_any.
    def visitType_any(self, ctx:TypeQLPythonParser.Type_anyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeQLPythonParser#type_scoped.
    def visitType_scoped(self, ctx:TypeQLPythonParser.Type_scopedContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeQLPythonParser#type_.
    def visitType_(self, ctx:TypeQLPythonParser.Type_Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeQLPythonParser#label_any.
    def visitLabel_any(self, ctx:TypeQLPythonParser.Label_anyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeQLPythonParser#label_scoped.
    def visitLabel_scoped(self, ctx:TypeQLPythonParser.Label_scopedContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeQLPythonParser#label.
    def visitLabel(self, ctx:TypeQLPythonParser.LabelContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeQLPythonParser#labels.
    def visitLabels(self, ctx:TypeQLPythonParser.LabelsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeQLPythonParser#label_array.
    def visitLabel_array(self, ctx:TypeQLPythonParser.Label_arrayContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeQLPythonParser#schema_native.
    def visitSchema_native(self, ctx:TypeQLPythonParser.Schema_nativeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeQLPythonParser#type_native.
    def visitType_native(self, ctx:TypeQLPythonParser.Type_nativeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeQLPythonParser#value_type.
    def visitValue_type(self, ctx:TypeQLPythonParser.Value_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeQLPythonParser#value.
    def visitValue(self, ctx:TypeQLPythonParser.ValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeQLPythonParser#regex.
    def visitRegex(self, ctx:TypeQLPythonParser.RegexContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeQLPythonParser#unreserved.
    def visitUnreserved(self, ctx:TypeQLPythonParser.UnreservedContext):
        return self.visitChildren(ctx)



del TypeQLPythonParser