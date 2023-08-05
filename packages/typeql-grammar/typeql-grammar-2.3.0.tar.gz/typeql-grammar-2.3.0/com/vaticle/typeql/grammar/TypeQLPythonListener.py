# Generated from /home/grabl/.cache/bazel/_bazel_grabl/7ef8d994fdedbcf15566d4e42e182314/sandbox/linux-sandbox/32/execroot/vaticle_typeql/bazel-out/k8-fastbuild/bin/grammar/TypeQLPython.g4 by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .TypeQLPythonParser import TypeQLPythonParser
else:
    from TypeQLPythonParser import TypeQLPythonParser

# This class defines a complete listener for a parse tree produced by TypeQLPythonParser.
class TypeQLPythonListener(ParseTreeListener):

    # Enter a parse tree produced by TypeQLPythonParser#eof_query.
    def enterEof_query(self, ctx:TypeQLPythonParser.Eof_queryContext):
        pass

    # Exit a parse tree produced by TypeQLPythonParser#eof_query.
    def exitEof_query(self, ctx:TypeQLPythonParser.Eof_queryContext):
        pass


    # Enter a parse tree produced by TypeQLPythonParser#eof_queries.
    def enterEof_queries(self, ctx:TypeQLPythonParser.Eof_queriesContext):
        pass

    # Exit a parse tree produced by TypeQLPythonParser#eof_queries.
    def exitEof_queries(self, ctx:TypeQLPythonParser.Eof_queriesContext):
        pass


    # Enter a parse tree produced by TypeQLPythonParser#eof_pattern.
    def enterEof_pattern(self, ctx:TypeQLPythonParser.Eof_patternContext):
        pass

    # Exit a parse tree produced by TypeQLPythonParser#eof_pattern.
    def exitEof_pattern(self, ctx:TypeQLPythonParser.Eof_patternContext):
        pass


    # Enter a parse tree produced by TypeQLPythonParser#eof_patterns.
    def enterEof_patterns(self, ctx:TypeQLPythonParser.Eof_patternsContext):
        pass

    # Exit a parse tree produced by TypeQLPythonParser#eof_patterns.
    def exitEof_patterns(self, ctx:TypeQLPythonParser.Eof_patternsContext):
        pass


    # Enter a parse tree produced by TypeQLPythonParser#eof_definables.
    def enterEof_definables(self, ctx:TypeQLPythonParser.Eof_definablesContext):
        pass

    # Exit a parse tree produced by TypeQLPythonParser#eof_definables.
    def exitEof_definables(self, ctx:TypeQLPythonParser.Eof_definablesContext):
        pass


    # Enter a parse tree produced by TypeQLPythonParser#eof_variable.
    def enterEof_variable(self, ctx:TypeQLPythonParser.Eof_variableContext):
        pass

    # Exit a parse tree produced by TypeQLPythonParser#eof_variable.
    def exitEof_variable(self, ctx:TypeQLPythonParser.Eof_variableContext):
        pass


    # Enter a parse tree produced by TypeQLPythonParser#eof_label.
    def enterEof_label(self, ctx:TypeQLPythonParser.Eof_labelContext):
        pass

    # Exit a parse tree produced by TypeQLPythonParser#eof_label.
    def exitEof_label(self, ctx:TypeQLPythonParser.Eof_labelContext):
        pass


    # Enter a parse tree produced by TypeQLPythonParser#eof_schema_rule.
    def enterEof_schema_rule(self, ctx:TypeQLPythonParser.Eof_schema_ruleContext):
        pass

    # Exit a parse tree produced by TypeQLPythonParser#eof_schema_rule.
    def exitEof_schema_rule(self, ctx:TypeQLPythonParser.Eof_schema_ruleContext):
        pass


    # Enter a parse tree produced by TypeQLPythonParser#query.
    def enterQuery(self, ctx:TypeQLPythonParser.QueryContext):
        pass

    # Exit a parse tree produced by TypeQLPythonParser#query.
    def exitQuery(self, ctx:TypeQLPythonParser.QueryContext):
        pass


    # Enter a parse tree produced by TypeQLPythonParser#query_define.
    def enterQuery_define(self, ctx:TypeQLPythonParser.Query_defineContext):
        pass

    # Exit a parse tree produced by TypeQLPythonParser#query_define.
    def exitQuery_define(self, ctx:TypeQLPythonParser.Query_defineContext):
        pass


    # Enter a parse tree produced by TypeQLPythonParser#query_undefine.
    def enterQuery_undefine(self, ctx:TypeQLPythonParser.Query_undefineContext):
        pass

    # Exit a parse tree produced by TypeQLPythonParser#query_undefine.
    def exitQuery_undefine(self, ctx:TypeQLPythonParser.Query_undefineContext):
        pass


    # Enter a parse tree produced by TypeQLPythonParser#query_insert.
    def enterQuery_insert(self, ctx:TypeQLPythonParser.Query_insertContext):
        pass

    # Exit a parse tree produced by TypeQLPythonParser#query_insert.
    def exitQuery_insert(self, ctx:TypeQLPythonParser.Query_insertContext):
        pass


    # Enter a parse tree produced by TypeQLPythonParser#query_delete_or_update.
    def enterQuery_delete_or_update(self, ctx:TypeQLPythonParser.Query_delete_or_updateContext):
        pass

    # Exit a parse tree produced by TypeQLPythonParser#query_delete_or_update.
    def exitQuery_delete_or_update(self, ctx:TypeQLPythonParser.Query_delete_or_updateContext):
        pass


    # Enter a parse tree produced by TypeQLPythonParser#query_match.
    def enterQuery_match(self, ctx:TypeQLPythonParser.Query_matchContext):
        pass

    # Exit a parse tree produced by TypeQLPythonParser#query_match.
    def exitQuery_match(self, ctx:TypeQLPythonParser.Query_matchContext):
        pass


    # Enter a parse tree produced by TypeQLPythonParser#query_compute.
    def enterQuery_compute(self, ctx:TypeQLPythonParser.Query_computeContext):
        pass

    # Exit a parse tree produced by TypeQLPythonParser#query_compute.
    def exitQuery_compute(self, ctx:TypeQLPythonParser.Query_computeContext):
        pass


    # Enter a parse tree produced by TypeQLPythonParser#query_match_aggregate.
    def enterQuery_match_aggregate(self, ctx:TypeQLPythonParser.Query_match_aggregateContext):
        pass

    # Exit a parse tree produced by TypeQLPythonParser#query_match_aggregate.
    def exitQuery_match_aggregate(self, ctx:TypeQLPythonParser.Query_match_aggregateContext):
        pass


    # Enter a parse tree produced by TypeQLPythonParser#query_match_group.
    def enterQuery_match_group(self, ctx:TypeQLPythonParser.Query_match_groupContext):
        pass

    # Exit a parse tree produced by TypeQLPythonParser#query_match_group.
    def exitQuery_match_group(self, ctx:TypeQLPythonParser.Query_match_groupContext):
        pass


    # Enter a parse tree produced by TypeQLPythonParser#query_match_group_agg.
    def enterQuery_match_group_agg(self, ctx:TypeQLPythonParser.Query_match_group_aggContext):
        pass

    # Exit a parse tree produced by TypeQLPythonParser#query_match_group_agg.
    def exitQuery_match_group_agg(self, ctx:TypeQLPythonParser.Query_match_group_aggContext):
        pass


    # Enter a parse tree produced by TypeQLPythonParser#modifiers.
    def enterModifiers(self, ctx:TypeQLPythonParser.ModifiersContext):
        pass

    # Exit a parse tree produced by TypeQLPythonParser#modifiers.
    def exitModifiers(self, ctx:TypeQLPythonParser.ModifiersContext):
        pass


    # Enter a parse tree produced by TypeQLPythonParser#filter_.
    def enterFilter_(self, ctx:TypeQLPythonParser.Filter_Context):
        pass

    # Exit a parse tree produced by TypeQLPythonParser#filter_.
    def exitFilter_(self, ctx:TypeQLPythonParser.Filter_Context):
        pass


    # Enter a parse tree produced by TypeQLPythonParser#sort.
    def enterSort(self, ctx:TypeQLPythonParser.SortContext):
        pass

    # Exit a parse tree produced by TypeQLPythonParser#sort.
    def exitSort(self, ctx:TypeQLPythonParser.SortContext):
        pass


    # Enter a parse tree produced by TypeQLPythonParser#offset.
    def enterOffset(self, ctx:TypeQLPythonParser.OffsetContext):
        pass

    # Exit a parse tree produced by TypeQLPythonParser#offset.
    def exitOffset(self, ctx:TypeQLPythonParser.OffsetContext):
        pass


    # Enter a parse tree produced by TypeQLPythonParser#limit.
    def enterLimit(self, ctx:TypeQLPythonParser.LimitContext):
        pass

    # Exit a parse tree produced by TypeQLPythonParser#limit.
    def exitLimit(self, ctx:TypeQLPythonParser.LimitContext):
        pass


    # Enter a parse tree produced by TypeQLPythonParser#match_aggregate.
    def enterMatch_aggregate(self, ctx:TypeQLPythonParser.Match_aggregateContext):
        pass

    # Exit a parse tree produced by TypeQLPythonParser#match_aggregate.
    def exitMatch_aggregate(self, ctx:TypeQLPythonParser.Match_aggregateContext):
        pass


    # Enter a parse tree produced by TypeQLPythonParser#aggregate_method.
    def enterAggregate_method(self, ctx:TypeQLPythonParser.Aggregate_methodContext):
        pass

    # Exit a parse tree produced by TypeQLPythonParser#aggregate_method.
    def exitAggregate_method(self, ctx:TypeQLPythonParser.Aggregate_methodContext):
        pass


    # Enter a parse tree produced by TypeQLPythonParser#match_group.
    def enterMatch_group(self, ctx:TypeQLPythonParser.Match_groupContext):
        pass

    # Exit a parse tree produced by TypeQLPythonParser#match_group.
    def exitMatch_group(self, ctx:TypeQLPythonParser.Match_groupContext):
        pass


    # Enter a parse tree produced by TypeQLPythonParser#definables.
    def enterDefinables(self, ctx:TypeQLPythonParser.DefinablesContext):
        pass

    # Exit a parse tree produced by TypeQLPythonParser#definables.
    def exitDefinables(self, ctx:TypeQLPythonParser.DefinablesContext):
        pass


    # Enter a parse tree produced by TypeQLPythonParser#definable.
    def enterDefinable(self, ctx:TypeQLPythonParser.DefinableContext):
        pass

    # Exit a parse tree produced by TypeQLPythonParser#definable.
    def exitDefinable(self, ctx:TypeQLPythonParser.DefinableContext):
        pass


    # Enter a parse tree produced by TypeQLPythonParser#patterns.
    def enterPatterns(self, ctx:TypeQLPythonParser.PatternsContext):
        pass

    # Exit a parse tree produced by TypeQLPythonParser#patterns.
    def exitPatterns(self, ctx:TypeQLPythonParser.PatternsContext):
        pass


    # Enter a parse tree produced by TypeQLPythonParser#pattern.
    def enterPattern(self, ctx:TypeQLPythonParser.PatternContext):
        pass

    # Exit a parse tree produced by TypeQLPythonParser#pattern.
    def exitPattern(self, ctx:TypeQLPythonParser.PatternContext):
        pass


    # Enter a parse tree produced by TypeQLPythonParser#pattern_conjunction.
    def enterPattern_conjunction(self, ctx:TypeQLPythonParser.Pattern_conjunctionContext):
        pass

    # Exit a parse tree produced by TypeQLPythonParser#pattern_conjunction.
    def exitPattern_conjunction(self, ctx:TypeQLPythonParser.Pattern_conjunctionContext):
        pass


    # Enter a parse tree produced by TypeQLPythonParser#pattern_disjunction.
    def enterPattern_disjunction(self, ctx:TypeQLPythonParser.Pattern_disjunctionContext):
        pass

    # Exit a parse tree produced by TypeQLPythonParser#pattern_disjunction.
    def exitPattern_disjunction(self, ctx:TypeQLPythonParser.Pattern_disjunctionContext):
        pass


    # Enter a parse tree produced by TypeQLPythonParser#pattern_negation.
    def enterPattern_negation(self, ctx:TypeQLPythonParser.Pattern_negationContext):
        pass

    # Exit a parse tree produced by TypeQLPythonParser#pattern_negation.
    def exitPattern_negation(self, ctx:TypeQLPythonParser.Pattern_negationContext):
        pass


    # Enter a parse tree produced by TypeQLPythonParser#pattern_variable.
    def enterPattern_variable(self, ctx:TypeQLPythonParser.Pattern_variableContext):
        pass

    # Exit a parse tree produced by TypeQLPythonParser#pattern_variable.
    def exitPattern_variable(self, ctx:TypeQLPythonParser.Pattern_variableContext):
        pass


    # Enter a parse tree produced by TypeQLPythonParser#variable_concept.
    def enterVariable_concept(self, ctx:TypeQLPythonParser.Variable_conceptContext):
        pass

    # Exit a parse tree produced by TypeQLPythonParser#variable_concept.
    def exitVariable_concept(self, ctx:TypeQLPythonParser.Variable_conceptContext):
        pass


    # Enter a parse tree produced by TypeQLPythonParser#variable_type.
    def enterVariable_type(self, ctx:TypeQLPythonParser.Variable_typeContext):
        pass

    # Exit a parse tree produced by TypeQLPythonParser#variable_type.
    def exitVariable_type(self, ctx:TypeQLPythonParser.Variable_typeContext):
        pass


    # Enter a parse tree produced by TypeQLPythonParser#type_constraint.
    def enterType_constraint(self, ctx:TypeQLPythonParser.Type_constraintContext):
        pass

    # Exit a parse tree produced by TypeQLPythonParser#type_constraint.
    def exitType_constraint(self, ctx:TypeQLPythonParser.Type_constraintContext):
        pass


    # Enter a parse tree produced by TypeQLPythonParser#variable_things.
    def enterVariable_things(self, ctx:TypeQLPythonParser.Variable_thingsContext):
        pass

    # Exit a parse tree produced by TypeQLPythonParser#variable_things.
    def exitVariable_things(self, ctx:TypeQLPythonParser.Variable_thingsContext):
        pass


    # Enter a parse tree produced by TypeQLPythonParser#variable_thing_any.
    def enterVariable_thing_any(self, ctx:TypeQLPythonParser.Variable_thing_anyContext):
        pass

    # Exit a parse tree produced by TypeQLPythonParser#variable_thing_any.
    def exitVariable_thing_any(self, ctx:TypeQLPythonParser.Variable_thing_anyContext):
        pass


    # Enter a parse tree produced by TypeQLPythonParser#variable_thing.
    def enterVariable_thing(self, ctx:TypeQLPythonParser.Variable_thingContext):
        pass

    # Exit a parse tree produced by TypeQLPythonParser#variable_thing.
    def exitVariable_thing(self, ctx:TypeQLPythonParser.Variable_thingContext):
        pass


    # Enter a parse tree produced by TypeQLPythonParser#variable_relation.
    def enterVariable_relation(self, ctx:TypeQLPythonParser.Variable_relationContext):
        pass

    # Exit a parse tree produced by TypeQLPythonParser#variable_relation.
    def exitVariable_relation(self, ctx:TypeQLPythonParser.Variable_relationContext):
        pass


    # Enter a parse tree produced by TypeQLPythonParser#variable_attribute.
    def enterVariable_attribute(self, ctx:TypeQLPythonParser.Variable_attributeContext):
        pass

    # Exit a parse tree produced by TypeQLPythonParser#variable_attribute.
    def exitVariable_attribute(self, ctx:TypeQLPythonParser.Variable_attributeContext):
        pass


    # Enter a parse tree produced by TypeQLPythonParser#relation.
    def enterRelation(self, ctx:TypeQLPythonParser.RelationContext):
        pass

    # Exit a parse tree produced by TypeQLPythonParser#relation.
    def exitRelation(self, ctx:TypeQLPythonParser.RelationContext):
        pass


    # Enter a parse tree produced by TypeQLPythonParser#role_player.
    def enterRole_player(self, ctx:TypeQLPythonParser.Role_playerContext):
        pass

    # Exit a parse tree produced by TypeQLPythonParser#role_player.
    def exitRole_player(self, ctx:TypeQLPythonParser.Role_playerContext):
        pass


    # Enter a parse tree produced by TypeQLPythonParser#player.
    def enterPlayer(self, ctx:TypeQLPythonParser.PlayerContext):
        pass

    # Exit a parse tree produced by TypeQLPythonParser#player.
    def exitPlayer(self, ctx:TypeQLPythonParser.PlayerContext):
        pass


    # Enter a parse tree produced by TypeQLPythonParser#attributes.
    def enterAttributes(self, ctx:TypeQLPythonParser.AttributesContext):
        pass

    # Exit a parse tree produced by TypeQLPythonParser#attributes.
    def exitAttributes(self, ctx:TypeQLPythonParser.AttributesContext):
        pass


    # Enter a parse tree produced by TypeQLPythonParser#attribute.
    def enterAttribute(self, ctx:TypeQLPythonParser.AttributeContext):
        pass

    # Exit a parse tree produced by TypeQLPythonParser#attribute.
    def exitAttribute(self, ctx:TypeQLPythonParser.AttributeContext):
        pass


    # Enter a parse tree produced by TypeQLPythonParser#predicate.
    def enterPredicate(self, ctx:TypeQLPythonParser.PredicateContext):
        pass

    # Exit a parse tree produced by TypeQLPythonParser#predicate.
    def exitPredicate(self, ctx:TypeQLPythonParser.PredicateContext):
        pass


    # Enter a parse tree produced by TypeQLPythonParser#predicate_equality.
    def enterPredicate_equality(self, ctx:TypeQLPythonParser.Predicate_equalityContext):
        pass

    # Exit a parse tree produced by TypeQLPythonParser#predicate_equality.
    def exitPredicate_equality(self, ctx:TypeQLPythonParser.Predicate_equalityContext):
        pass


    # Enter a parse tree produced by TypeQLPythonParser#predicate_substring.
    def enterPredicate_substring(self, ctx:TypeQLPythonParser.Predicate_substringContext):
        pass

    # Exit a parse tree produced by TypeQLPythonParser#predicate_substring.
    def exitPredicate_substring(self, ctx:TypeQLPythonParser.Predicate_substringContext):
        pass


    # Enter a parse tree produced by TypeQLPythonParser#predicate_value.
    def enterPredicate_value(self, ctx:TypeQLPythonParser.Predicate_valueContext):
        pass

    # Exit a parse tree produced by TypeQLPythonParser#predicate_value.
    def exitPredicate_value(self, ctx:TypeQLPythonParser.Predicate_valueContext):
        pass


    # Enter a parse tree produced by TypeQLPythonParser#schema_rule.
    def enterSchema_rule(self, ctx:TypeQLPythonParser.Schema_ruleContext):
        pass

    # Exit a parse tree produced by TypeQLPythonParser#schema_rule.
    def exitSchema_rule(self, ctx:TypeQLPythonParser.Schema_ruleContext):
        pass


    # Enter a parse tree produced by TypeQLPythonParser#compute_conditions.
    def enterCompute_conditions(self, ctx:TypeQLPythonParser.Compute_conditionsContext):
        pass

    # Exit a parse tree produced by TypeQLPythonParser#compute_conditions.
    def exitCompute_conditions(self, ctx:TypeQLPythonParser.Compute_conditionsContext):
        pass


    # Enter a parse tree produced by TypeQLPythonParser#compute_method.
    def enterCompute_method(self, ctx:TypeQLPythonParser.Compute_methodContext):
        pass

    # Exit a parse tree produced by TypeQLPythonParser#compute_method.
    def exitCompute_method(self, ctx:TypeQLPythonParser.Compute_methodContext):
        pass


    # Enter a parse tree produced by TypeQLPythonParser#conditions_count.
    def enterConditions_count(self, ctx:TypeQLPythonParser.Conditions_countContext):
        pass

    # Exit a parse tree produced by TypeQLPythonParser#conditions_count.
    def exitConditions_count(self, ctx:TypeQLPythonParser.Conditions_countContext):
        pass


    # Enter a parse tree produced by TypeQLPythonParser#conditions_value.
    def enterConditions_value(self, ctx:TypeQLPythonParser.Conditions_valueContext):
        pass

    # Exit a parse tree produced by TypeQLPythonParser#conditions_value.
    def exitConditions_value(self, ctx:TypeQLPythonParser.Conditions_valueContext):
        pass


    # Enter a parse tree produced by TypeQLPythonParser#conditions_central.
    def enterConditions_central(self, ctx:TypeQLPythonParser.Conditions_centralContext):
        pass

    # Exit a parse tree produced by TypeQLPythonParser#conditions_central.
    def exitConditions_central(self, ctx:TypeQLPythonParser.Conditions_centralContext):
        pass


    # Enter a parse tree produced by TypeQLPythonParser#conditions_cluster.
    def enterConditions_cluster(self, ctx:TypeQLPythonParser.Conditions_clusterContext):
        pass

    # Exit a parse tree produced by TypeQLPythonParser#conditions_cluster.
    def exitConditions_cluster(self, ctx:TypeQLPythonParser.Conditions_clusterContext):
        pass


    # Enter a parse tree produced by TypeQLPythonParser#conditions_path.
    def enterConditions_path(self, ctx:TypeQLPythonParser.Conditions_pathContext):
        pass

    # Exit a parse tree produced by TypeQLPythonParser#conditions_path.
    def exitConditions_path(self, ctx:TypeQLPythonParser.Conditions_pathContext):
        pass


    # Enter a parse tree produced by TypeQLPythonParser#input_count.
    def enterInput_count(self, ctx:TypeQLPythonParser.Input_countContext):
        pass

    # Exit a parse tree produced by TypeQLPythonParser#input_count.
    def exitInput_count(self, ctx:TypeQLPythonParser.Input_countContext):
        pass


    # Enter a parse tree produced by TypeQLPythonParser#input_value.
    def enterInput_value(self, ctx:TypeQLPythonParser.Input_valueContext):
        pass

    # Exit a parse tree produced by TypeQLPythonParser#input_value.
    def exitInput_value(self, ctx:TypeQLPythonParser.Input_valueContext):
        pass


    # Enter a parse tree produced by TypeQLPythonParser#input_central.
    def enterInput_central(self, ctx:TypeQLPythonParser.Input_centralContext):
        pass

    # Exit a parse tree produced by TypeQLPythonParser#input_central.
    def exitInput_central(self, ctx:TypeQLPythonParser.Input_centralContext):
        pass


    # Enter a parse tree produced by TypeQLPythonParser#input_cluster.
    def enterInput_cluster(self, ctx:TypeQLPythonParser.Input_clusterContext):
        pass

    # Exit a parse tree produced by TypeQLPythonParser#input_cluster.
    def exitInput_cluster(self, ctx:TypeQLPythonParser.Input_clusterContext):
        pass


    # Enter a parse tree produced by TypeQLPythonParser#input_path.
    def enterInput_path(self, ctx:TypeQLPythonParser.Input_pathContext):
        pass

    # Exit a parse tree produced by TypeQLPythonParser#input_path.
    def exitInput_path(self, ctx:TypeQLPythonParser.Input_pathContext):
        pass


    # Enter a parse tree produced by TypeQLPythonParser#compute_direction.
    def enterCompute_direction(self, ctx:TypeQLPythonParser.Compute_directionContext):
        pass

    # Exit a parse tree produced by TypeQLPythonParser#compute_direction.
    def exitCompute_direction(self, ctx:TypeQLPythonParser.Compute_directionContext):
        pass


    # Enter a parse tree produced by TypeQLPythonParser#compute_target.
    def enterCompute_target(self, ctx:TypeQLPythonParser.Compute_targetContext):
        pass

    # Exit a parse tree produced by TypeQLPythonParser#compute_target.
    def exitCompute_target(self, ctx:TypeQLPythonParser.Compute_targetContext):
        pass


    # Enter a parse tree produced by TypeQLPythonParser#compute_scope.
    def enterCompute_scope(self, ctx:TypeQLPythonParser.Compute_scopeContext):
        pass

    # Exit a parse tree produced by TypeQLPythonParser#compute_scope.
    def exitCompute_scope(self, ctx:TypeQLPythonParser.Compute_scopeContext):
        pass


    # Enter a parse tree produced by TypeQLPythonParser#compute_config.
    def enterCompute_config(self, ctx:TypeQLPythonParser.Compute_configContext):
        pass

    # Exit a parse tree produced by TypeQLPythonParser#compute_config.
    def exitCompute_config(self, ctx:TypeQLPythonParser.Compute_configContext):
        pass


    # Enter a parse tree produced by TypeQLPythonParser#compute_algorithm.
    def enterCompute_algorithm(self, ctx:TypeQLPythonParser.Compute_algorithmContext):
        pass

    # Exit a parse tree produced by TypeQLPythonParser#compute_algorithm.
    def exitCompute_algorithm(self, ctx:TypeQLPythonParser.Compute_algorithmContext):
        pass


    # Enter a parse tree produced by TypeQLPythonParser#compute_args.
    def enterCompute_args(self, ctx:TypeQLPythonParser.Compute_argsContext):
        pass

    # Exit a parse tree produced by TypeQLPythonParser#compute_args.
    def exitCompute_args(self, ctx:TypeQLPythonParser.Compute_argsContext):
        pass


    # Enter a parse tree produced by TypeQLPythonParser#compute_args_array.
    def enterCompute_args_array(self, ctx:TypeQLPythonParser.Compute_args_arrayContext):
        pass

    # Exit a parse tree produced by TypeQLPythonParser#compute_args_array.
    def exitCompute_args_array(self, ctx:TypeQLPythonParser.Compute_args_arrayContext):
        pass


    # Enter a parse tree produced by TypeQLPythonParser#compute_arg.
    def enterCompute_arg(self, ctx:TypeQLPythonParser.Compute_argContext):
        pass

    # Exit a parse tree produced by TypeQLPythonParser#compute_arg.
    def exitCompute_arg(self, ctx:TypeQLPythonParser.Compute_argContext):
        pass


    # Enter a parse tree produced by TypeQLPythonParser#type_any.
    def enterType_any(self, ctx:TypeQLPythonParser.Type_anyContext):
        pass

    # Exit a parse tree produced by TypeQLPythonParser#type_any.
    def exitType_any(self, ctx:TypeQLPythonParser.Type_anyContext):
        pass


    # Enter a parse tree produced by TypeQLPythonParser#type_scoped.
    def enterType_scoped(self, ctx:TypeQLPythonParser.Type_scopedContext):
        pass

    # Exit a parse tree produced by TypeQLPythonParser#type_scoped.
    def exitType_scoped(self, ctx:TypeQLPythonParser.Type_scopedContext):
        pass


    # Enter a parse tree produced by TypeQLPythonParser#type_.
    def enterType_(self, ctx:TypeQLPythonParser.Type_Context):
        pass

    # Exit a parse tree produced by TypeQLPythonParser#type_.
    def exitType_(self, ctx:TypeQLPythonParser.Type_Context):
        pass


    # Enter a parse tree produced by TypeQLPythonParser#label_any.
    def enterLabel_any(self, ctx:TypeQLPythonParser.Label_anyContext):
        pass

    # Exit a parse tree produced by TypeQLPythonParser#label_any.
    def exitLabel_any(self, ctx:TypeQLPythonParser.Label_anyContext):
        pass


    # Enter a parse tree produced by TypeQLPythonParser#label_scoped.
    def enterLabel_scoped(self, ctx:TypeQLPythonParser.Label_scopedContext):
        pass

    # Exit a parse tree produced by TypeQLPythonParser#label_scoped.
    def exitLabel_scoped(self, ctx:TypeQLPythonParser.Label_scopedContext):
        pass


    # Enter a parse tree produced by TypeQLPythonParser#label.
    def enterLabel(self, ctx:TypeQLPythonParser.LabelContext):
        pass

    # Exit a parse tree produced by TypeQLPythonParser#label.
    def exitLabel(self, ctx:TypeQLPythonParser.LabelContext):
        pass


    # Enter a parse tree produced by TypeQLPythonParser#labels.
    def enterLabels(self, ctx:TypeQLPythonParser.LabelsContext):
        pass

    # Exit a parse tree produced by TypeQLPythonParser#labels.
    def exitLabels(self, ctx:TypeQLPythonParser.LabelsContext):
        pass


    # Enter a parse tree produced by TypeQLPythonParser#label_array.
    def enterLabel_array(self, ctx:TypeQLPythonParser.Label_arrayContext):
        pass

    # Exit a parse tree produced by TypeQLPythonParser#label_array.
    def exitLabel_array(self, ctx:TypeQLPythonParser.Label_arrayContext):
        pass


    # Enter a parse tree produced by TypeQLPythonParser#schema_native.
    def enterSchema_native(self, ctx:TypeQLPythonParser.Schema_nativeContext):
        pass

    # Exit a parse tree produced by TypeQLPythonParser#schema_native.
    def exitSchema_native(self, ctx:TypeQLPythonParser.Schema_nativeContext):
        pass


    # Enter a parse tree produced by TypeQLPythonParser#type_native.
    def enterType_native(self, ctx:TypeQLPythonParser.Type_nativeContext):
        pass

    # Exit a parse tree produced by TypeQLPythonParser#type_native.
    def exitType_native(self, ctx:TypeQLPythonParser.Type_nativeContext):
        pass


    # Enter a parse tree produced by TypeQLPythonParser#value_type.
    def enterValue_type(self, ctx:TypeQLPythonParser.Value_typeContext):
        pass

    # Exit a parse tree produced by TypeQLPythonParser#value_type.
    def exitValue_type(self, ctx:TypeQLPythonParser.Value_typeContext):
        pass


    # Enter a parse tree produced by TypeQLPythonParser#value.
    def enterValue(self, ctx:TypeQLPythonParser.ValueContext):
        pass

    # Exit a parse tree produced by TypeQLPythonParser#value.
    def exitValue(self, ctx:TypeQLPythonParser.ValueContext):
        pass


    # Enter a parse tree produced by TypeQLPythonParser#regex.
    def enterRegex(self, ctx:TypeQLPythonParser.RegexContext):
        pass

    # Exit a parse tree produced by TypeQLPythonParser#regex.
    def exitRegex(self, ctx:TypeQLPythonParser.RegexContext):
        pass


    # Enter a parse tree produced by TypeQLPythonParser#unreserved.
    def enterUnreserved(self, ctx:TypeQLPythonParser.UnreservedContext):
        pass

    # Exit a parse tree produced by TypeQLPythonParser#unreserved.
    def exitUnreserved(self, ctx:TypeQLPythonParser.UnreservedContext):
        pass


