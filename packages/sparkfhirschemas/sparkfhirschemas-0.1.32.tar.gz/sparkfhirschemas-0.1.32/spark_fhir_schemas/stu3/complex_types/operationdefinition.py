from typing import Union, List, Optional

from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    ArrayType,
    BooleanType,
    DataType,
)


# This file is auto-generated by generate_schema so do not edit manually
# noinspection PyPep8Naming
class OperationDefinitionSchema:
    """
    A formal computable definition of an operation (on the RESTful interface) or a
    named query (using the search interaction).
    """

    # noinspection PyDefaultArgument
    @staticmethod
    def get_schema(
        max_nesting_depth: Optional[int] = 6,
        nesting_depth: int = 0,
        nesting_list: List[str] = [],
        max_recursion_limit: Optional[int] = 2,
        include_extension: Optional[bool] = False,
        extension_fields: Optional[List[str]] = [
            "valueBoolean",
            "valueCode",
            "valueDate",
            "valueDateTime",
            "valueDecimal",
            "valueId",
            "valueInteger",
            "valuePositiveInt",
            "valueString",
            "valueTime",
            "valueUnsignedInt",
            "valueUri",
            "valueQuantity",
        ],
        extension_depth: int = 0,
        max_extension_depth: Optional[int] = 2,
    ) -> Union[StructType, DataType]:
        """
        A formal computable definition of an operation (on the RESTful interface) or a
        named query (using the search interaction).


        id: The logical id of the resource, as used in the URL for the resource. Once
            assigned, this value never changes.

        extension: May be used to represent additional information that is not part of the basic
            definition of the resource. In order to make the use of extensions safe and
            manageable, there is a strict set of governance  applied to the definition and
            use of extensions. Though any implementer is allowed to define an extension,
            there is a set of requirements that SHALL be met as part of the definition of
            the extension.

        meta: The metadata about the resource. This is content that is maintained by the
            infrastructure. Changes to the content may not always be associated with
            version changes to the resource.

        implicitRules: A reference to a set of rules that were followed when the resource was
            constructed, and which must be understood when processing the content.

        language: The base language in which the resource is written.

        text: A human-readable narrative that contains a summary of the resource, and may be
            used to represent the content of the resource to a human. The narrative need
            not encode all the structured data, but is required to contain sufficient
            detail to make it "clinically safe" for a human to just read the narrative.
            Resource definitions may define what content should be represented in the
            narrative to ensure clinical safety.

        contained: These resources do not have an independent existence apart from the resource
            that contains them - they cannot be identified independently, and nor can they
            have their own independent transaction scope.

        resourceType: This is a OperationDefinition resource

        url: An absolute URI that is used to identify this operation definition when it is
            referenced in a specification, model, design or an instance. This SHALL be a
            URL, SHOULD be globally unique, and SHOULD be an address at which this
            operation definition is (or will be) published. The URL SHOULD include the
            major version of the operation definition. For more information see [Technical
            and Business Versions](resource.html#versions).

        version: The identifier that is used to identify this version of the operation
            definition when it is referenced in a specification, model, design or
            instance. This is an arbitrary value managed by the operation definition
            author and is not expected to be globally unique. For example, it might be a
            timestamp (e.g. yyyymmdd) if a managed version is not available. There is also
            no expectation that versions can be placed in a lexicographical sequence.

        name: A natural language name identifying the operation definition. This name should
            be usable as an identifier for the module by machine processing applications
            such as code generation.

        status: The status of this operation definition. Enables tracking the life-cycle of
            the content.

        kind: Whether this is an operation or a named query.

        experimental: A boolean value to indicate that this operation definition is authored for
            testing purposes (or education/evaluation/marketing), and is not intended to
            be used for genuine usage.

        date: The date  (and optionally time) when the operation definition was published.
            The date must change if and when the business version changes and it must
            change if the status code changes. In addition, it should change when the
            substantive content of the operation definition changes.

        publisher: The name of the individual or organization that published the operation
            definition.

        contact: Contact details to assist a user in finding and communicating with the
            publisher.

        description: A free text natural language description of the operation definition from a
            consumer's perspective.

        useContext: The content was developed with a focus and intent of supporting the contexts
            that are listed. These terms may be used to assist with indexing and searching
            for appropriate operation definition instances.

        jurisdiction: A legal or geographic region in which the operation definition is intended to
            be used.

        purpose: Explaination of why this operation definition is needed and why it has been
            designed as it has.

        idempotent: Operations that are idempotent (see [HTTP specification definition of
            idempotent](http://www.w3.org/Protocols/rfc2616/rfc2616-sec9.html)) may be
            invoked by performing an HTTP GET operation instead of a POST.

        code: The name used to invoke the operation.

        comment: Additional information about how to use this operation or named query.

        base: Indicates that this operation definition is a constraining profile on the
            base.

        resource: The types on which this operation can be executed.

        system: Indicates whether this operation or named query can be invoked at the system
            level (e.g. without needing to choose a resource type for the context).

        type: Indicates whether this operation or named query can be invoked at the resource
            type level for any given resource type level (e.g. without needing to choose a
            specific resource id for the context).

        instance: Indicates whether this operation can be invoked on a particular instance of
            one of the given types.

        parameter: The parameters for the operation/query.

        overload: Defines an appropriate combination of parameters to use when invoking this
            operation, to help code generators when generating overloaded parameter sets
            for this operation.

        """
        from spark_fhir_schemas.stu3.complex_types.extension import ExtensionSchema
        from spark_fhir_schemas.stu3.complex_types.meta import MetaSchema
        from spark_fhir_schemas.stu3.complex_types.narrative import NarrativeSchema
        from spark_fhir_schemas.stu3.simple_types.resourcelist import ResourceListSchema
        from spark_fhir_schemas.stu3.complex_types.contactdetail import (
            ContactDetailSchema,
        )
        from spark_fhir_schemas.stu3.complex_types.usagecontext import (
            UsageContextSchema,
        )
        from spark_fhir_schemas.stu3.complex_types.codeableconcept import (
            CodeableConceptSchema,
        )
        from spark_fhir_schemas.stu3.complex_types.reference import ReferenceSchema
        from spark_fhir_schemas.stu3.complex_types.operationdefinition_parameter import (
            OperationDefinition_ParameterSchema,
        )
        from spark_fhir_schemas.stu3.complex_types.operationdefinition_overload import (
            OperationDefinition_OverloadSchema,
        )

        if (
            max_recursion_limit
            and nesting_list.count("OperationDefinition") >= max_recursion_limit
        ) or (max_nesting_depth and nesting_depth >= max_nesting_depth):
            return StructType([StructField("id", StringType(), True)])
        # add my name to recursion list for later
        my_nesting_list: List[str] = nesting_list + ["OperationDefinition"]
        schema = StructType(
            [
                # The logical id of the resource, as used in the URL for the resource. Once
                # assigned, this value never changes.
                StructField("id", StringType(), True),
                # May be used to represent additional information that is not part of the basic
                # definition of the resource. In order to make the use of extensions safe and
                # manageable, there is a strict set of governance  applied to the definition and
                # use of extensions. Though any implementer is allowed to define an extension,
                # there is a set of requirements that SHALL be met as part of the definition of
                # the extension.
                StructField(
                    "extension",
                    ArrayType(
                        ExtensionSchema.get_schema(
                            max_nesting_depth=max_nesting_depth,
                            nesting_depth=nesting_depth + 1,
                            nesting_list=my_nesting_list,
                            max_recursion_limit=max_recursion_limit,
                            include_extension=include_extension,
                            extension_fields=extension_fields,
                            extension_depth=extension_depth,
                            max_extension_depth=max_extension_depth,
                        )
                    ),
                    True,
                ),
                # The metadata about the resource. This is content that is maintained by the
                # infrastructure. Changes to the content may not always be associated with
                # version changes to the resource.
                StructField(
                    "meta",
                    MetaSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension,
                        extension_fields=extension_fields,
                        extension_depth=extension_depth + 1,
                        max_extension_depth=max_extension_depth,
                    ),
                    True,
                ),
                # A reference to a set of rules that were followed when the resource was
                # constructed, and which must be understood when processing the content.
                StructField("implicitRules", StringType(), True),
                # The base language in which the resource is written.
                StructField("language", StringType(), True),
                # A human-readable narrative that contains a summary of the resource, and may be
                # used to represent the content of the resource to a human. The narrative need
                # not encode all the structured data, but is required to contain sufficient
                # detail to make it "clinically safe" for a human to just read the narrative.
                # Resource definitions may define what content should be represented in the
                # narrative to ensure clinical safety.
                StructField(
                    "text",
                    NarrativeSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension,
                        extension_fields=extension_fields,
                        extension_depth=extension_depth + 1,
                        max_extension_depth=max_extension_depth,
                    ),
                    True,
                ),
                # These resources do not have an independent existence apart from the resource
                # that contains them - they cannot be identified independently, and nor can they
                # have their own independent transaction scope.
                StructField(
                    "contained",
                    ArrayType(
                        ResourceListSchema.get_schema(
                            max_nesting_depth=max_nesting_depth,
                            nesting_depth=nesting_depth + 1,
                            nesting_list=my_nesting_list,
                            max_recursion_limit=max_recursion_limit,
                            include_extension=include_extension,
                            extension_fields=extension_fields,
                            extension_depth=extension_depth,
                            max_extension_depth=max_extension_depth,
                        )
                    ),
                    True,
                ),
                # This is a OperationDefinition resource
                StructField("resourceType", StringType(), True),
                # An absolute URI that is used to identify this operation definition when it is
                # referenced in a specification, model, design or an instance. This SHALL be a
                # URL, SHOULD be globally unique, and SHOULD be an address at which this
                # operation definition is (or will be) published. The URL SHOULD include the
                # major version of the operation definition. For more information see [Technical
                # and Business Versions](resource.html#versions).
                StructField("url", StringType(), True),
                # The identifier that is used to identify this version of the operation
                # definition when it is referenced in a specification, model, design or
                # instance. This is an arbitrary value managed by the operation definition
                # author and is not expected to be globally unique. For example, it might be a
                # timestamp (e.g. yyyymmdd) if a managed version is not available. There is also
                # no expectation that versions can be placed in a lexicographical sequence.
                StructField("version", StringType(), True),
                # A natural language name identifying the operation definition. This name should
                # be usable as an identifier for the module by machine processing applications
                # such as code generation.
                StructField("name", StringType(), True),
                # The status of this operation definition. Enables tracking the life-cycle of
                # the content.
                StructField("status", StringType(), True),
                # Whether this is an operation or a named query.
                StructField("kind", StringType(), True),
                # A boolean value to indicate that this operation definition is authored for
                # testing purposes (or education/evaluation/marketing), and is not intended to
                # be used for genuine usage.
                StructField("experimental", BooleanType(), True),
                # The date  (and optionally time) when the operation definition was published.
                # The date must change if and when the business version changes and it must
                # change if the status code changes. In addition, it should change when the
                # substantive content of the operation definition changes.
                StructField("date", StringType(), True),
                # The name of the individual or organization that published the operation
                # definition.
                StructField("publisher", StringType(), True),
                # Contact details to assist a user in finding and communicating with the
                # publisher.
                StructField(
                    "contact",
                    ArrayType(
                        ContactDetailSchema.get_schema(
                            max_nesting_depth=max_nesting_depth,
                            nesting_depth=nesting_depth + 1,
                            nesting_list=my_nesting_list,
                            max_recursion_limit=max_recursion_limit,
                            include_extension=include_extension,
                            extension_fields=extension_fields,
                            extension_depth=extension_depth,
                            max_extension_depth=max_extension_depth,
                        )
                    ),
                    True,
                ),
                # A free text natural language description of the operation definition from a
                # consumer's perspective.
                StructField("description", StringType(), True),
                # The content was developed with a focus and intent of supporting the contexts
                # that are listed. These terms may be used to assist with indexing and searching
                # for appropriate operation definition instances.
                StructField(
                    "useContext",
                    ArrayType(
                        UsageContextSchema.get_schema(
                            max_nesting_depth=max_nesting_depth,
                            nesting_depth=nesting_depth + 1,
                            nesting_list=my_nesting_list,
                            max_recursion_limit=max_recursion_limit,
                            include_extension=include_extension,
                            extension_fields=extension_fields,
                            extension_depth=extension_depth,
                            max_extension_depth=max_extension_depth,
                        )
                    ),
                    True,
                ),
                # A legal or geographic region in which the operation definition is intended to
                # be used.
                StructField(
                    "jurisdiction",
                    ArrayType(
                        CodeableConceptSchema.get_schema(
                            max_nesting_depth=max_nesting_depth,
                            nesting_depth=nesting_depth + 1,
                            nesting_list=my_nesting_list,
                            max_recursion_limit=max_recursion_limit,
                            include_extension=include_extension,
                            extension_fields=extension_fields,
                            extension_depth=extension_depth,
                            max_extension_depth=max_extension_depth,
                        )
                    ),
                    True,
                ),
                # Explaination of why this operation definition is needed and why it has been
                # designed as it has.
                StructField("purpose", StringType(), True),
                # Operations that are idempotent (see [HTTP specification definition of
                # idempotent](http://www.w3.org/Protocols/rfc2616/rfc2616-sec9.html)) may be
                # invoked by performing an HTTP GET operation instead of a POST.
                StructField("idempotent", BooleanType(), True),
                # The name used to invoke the operation.
                StructField("code", StringType(), True),
                # Additional information about how to use this operation or named query.
                StructField("comment", StringType(), True),
                # Indicates that this operation definition is a constraining profile on the
                # base.
                StructField(
                    "base",
                    ReferenceSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension,
                        extension_fields=extension_fields,
                        extension_depth=extension_depth + 1,
                        max_extension_depth=max_extension_depth,
                    ),
                    True,
                ),
                # The types on which this operation can be executed.
                # Indicates whether this operation or named query can be invoked at the system
                # level (e.g. without needing to choose a resource type for the context).
                StructField("system", BooleanType(), True),
                # Indicates whether this operation or named query can be invoked at the resource
                # type level for any given resource type level (e.g. without needing to choose a
                # specific resource id for the context).
                StructField("type", BooleanType(), True),
                # Indicates whether this operation can be invoked on a particular instance of
                # one of the given types.
                StructField("instance", BooleanType(), True),
                # The parameters for the operation/query.
                StructField(
                    "parameter",
                    ArrayType(
                        OperationDefinition_ParameterSchema.get_schema(
                            max_nesting_depth=max_nesting_depth,
                            nesting_depth=nesting_depth + 1,
                            nesting_list=my_nesting_list,
                            max_recursion_limit=max_recursion_limit,
                            include_extension=include_extension,
                            extension_fields=extension_fields,
                            extension_depth=extension_depth,
                            max_extension_depth=max_extension_depth,
                        )
                    ),
                    True,
                ),
                # Defines an appropriate combination of parameters to use when invoking this
                # operation, to help code generators when generating overloaded parameter sets
                # for this operation.
                StructField(
                    "overload",
                    ArrayType(
                        OperationDefinition_OverloadSchema.get_schema(
                            max_nesting_depth=max_nesting_depth,
                            nesting_depth=nesting_depth + 1,
                            nesting_list=my_nesting_list,
                            max_recursion_limit=max_recursion_limit,
                            include_extension=include_extension,
                            extension_fields=extension_fields,
                            extension_depth=extension_depth,
                            max_extension_depth=max_extension_depth,
                        )
                    ),
                    True,
                ),
            ]
        )
        if not include_extension:
            schema.fields = [
                c
                if c.name != "extension"
                else StructField("extension", StringType(), True)
                for c in schema.fields
            ]

        return schema
