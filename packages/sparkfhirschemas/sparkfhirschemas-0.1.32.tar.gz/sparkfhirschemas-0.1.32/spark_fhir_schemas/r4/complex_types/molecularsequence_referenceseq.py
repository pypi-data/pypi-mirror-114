from typing import Union, List, Optional

from pyspark.sql.types import StructType, StructField, StringType, ArrayType, DataType


# This file is auto-generated by generate_schema so do not edit it manually
# noinspection PyPep8Naming
class MolecularSequence_ReferenceSeqSchema:
    """
    Raw data describing a biological sequence.
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
            "valueUrl",
        ],
        extension_depth: int = 0,
        max_extension_depth: Optional[int] = 2,
        include_modifierExtension: Optional[bool] = False,
    ) -> Union[StructType, DataType]:
        """
        Raw data describing a biological sequence.


        id: Unique id for the element within a resource (for internal references). This
            may be any string value that does not contain spaces.

        extension: May be used to represent additional information that is not part of the basic
            definition of the element. To make the use of extensions safe and manageable,
            there is a strict set of governance  applied to the definition and use of
            extensions. Though any implementer can define an extension, there is a set of
            requirements that SHALL be met as part of the definition of the extension.

        modifierExtension: May be used to represent additional information that is not part of the basic
            definition of the element and that modifies the understanding of the element
            in which it is contained and/or the understanding of the containing element's
            descendants. Usually modifier elements provide negation or qualification. To
            make the use of extensions safe and manageable, there is a strict set of
            governance applied to the definition and use of extensions. Though any
            implementer can define an extension, there is a set of requirements that SHALL
            be met as part of the definition of the extension. Applications processing a
            resource are required to check for modifier extensions.

            Modifier extensions SHALL NOT change the meaning of any elements on Resource
            or DomainResource (including cannot change the meaning of modifierExtension
            itself).

        chromosome: Structural unit composed of a nucleic acid molecule which controls its own
            replication through the interaction of specific proteins at one or more
            origins of replication ([SO:0000340](http://www.sequenceontology.org/browser/c
            urrent_svn/term/SO:0000340)).

        genomeBuild: The Genome Build used for reference, following GRCh build versions e.g. 'GRCh
            37'.  Version number must be included if a versioned release of a primary
            build was used.

        orientation: A relative reference to a DNA strand based on gene orientation. The strand
            that contains the open reading frame of the gene is the "sense" strand, and
            the opposite complementary strand is the "antisense" strand.

        referenceSeqId: Reference identifier of reference sequence submitted to NCBI. It must match
            the type in the MolecularSequence.type field. For example, the prefix, “NG_”
            identifies reference sequence for genes, “NM_” for messenger RNA transcripts,
            and “NP_” for amino acid sequences.

        referenceSeqPointer: A pointer to another MolecularSequence entity as reference sequence.

        referenceSeqString: A string like "ACGT".

        strand: An absolute reference to a strand. The Watson strand is the strand whose
            5'-end is on the short arm of the chromosome, and the Crick strand as the one
            whose 5'-end is on the long arm.

        windowStart: Start position of the window on the reference sequence. If the coordinate
            system is either 0-based or 1-based, then start position is inclusive.

        windowEnd: End position of the window on the reference sequence. If the coordinate system
            is 0-based then end is exclusive and does not include the last position. If
            the coordinate system is 1-base, then end is inclusive and includes the last
            position.

        """
        from spark_fhir_schemas.r4.complex_types.extension import ExtensionSchema
        from spark_fhir_schemas.r4.complex_types.codeableconcept import (
            CodeableConceptSchema,
        )
        from spark_fhir_schemas.r4.complex_types.reference import ReferenceSchema
        from spark_fhir_schemas.r4.simple_types.integer import integerSchema

        if (
            max_recursion_limit
            and nesting_list.count("MolecularSequence_ReferenceSeq")
            >= max_recursion_limit
        ) or (max_nesting_depth and nesting_depth >= max_nesting_depth):
            return StructType([StructField("id", StringType(), True)])
        # add my name to recursion list for later
        my_nesting_list: List[str] = nesting_list + ["MolecularSequence_ReferenceSeq"]
        schema = StructType(
            [
                # Unique id for the element within a resource (for internal references). This
                # may be any string value that does not contain spaces.
                StructField("id", StringType(), True),
                # May be used to represent additional information that is not part of the basic
                # definition of the element. To make the use of extensions safe and manageable,
                # there is a strict set of governance  applied to the definition and use of
                # extensions. Though any implementer can define an extension, there is a set of
                # requirements that SHALL be met as part of the definition of the extension.
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
                            include_modifierExtension=include_modifierExtension,
                        )
                    ),
                    True,
                ),
                # May be used to represent additional information that is not part of the basic
                # definition of the element and that modifies the understanding of the element
                # in which it is contained and/or the understanding of the containing element's
                # descendants. Usually modifier elements provide negation or qualification. To
                # make the use of extensions safe and manageable, there is a strict set of
                # governance applied to the definition and use of extensions. Though any
                # implementer can define an extension, there is a set of requirements that SHALL
                # be met as part of the definition of the extension. Applications processing a
                # resource are required to check for modifier extensions.
                #
                # Modifier extensions SHALL NOT change the meaning of any elements on Resource
                # or DomainResource (including cannot change the meaning of modifierExtension
                # itself).
                StructField(
                    "modifierExtension",
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
                            include_modifierExtension=include_modifierExtension,
                        )
                    ),
                    True,
                ),
                # Structural unit composed of a nucleic acid molecule which controls its own
                # replication through the interaction of specific proteins at one or more
                # origins of replication ([SO:0000340](http://www.sequenceontology.org/browser/c
                # urrent_svn/term/SO:0000340)).
                StructField(
                    "chromosome",
                    CodeableConceptSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension,
                        extension_fields=extension_fields,
                        extension_depth=extension_depth + 1,
                        max_extension_depth=max_extension_depth,
                        include_modifierExtension=include_modifierExtension,
                    ),
                    True,
                ),
                # The Genome Build used for reference, following GRCh build versions e.g. 'GRCh
                # 37'.  Version number must be included if a versioned release of a primary
                # build was used.
                StructField("genomeBuild", StringType(), True),
                # A relative reference to a DNA strand based on gene orientation. The strand
                # that contains the open reading frame of the gene is the "sense" strand, and
                # the opposite complementary strand is the "antisense" strand.
                StructField("orientation", StringType(), True),
                # Reference identifier of reference sequence submitted to NCBI. It must match
                # the type in the MolecularSequence.type field. For example, the prefix, “NG_”
                # identifies reference sequence for genes, “NM_” for messenger RNA transcripts,
                # and “NP_” for amino acid sequences.
                StructField(
                    "referenceSeqId",
                    CodeableConceptSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension,
                        extension_fields=extension_fields,
                        extension_depth=extension_depth + 1,
                        max_extension_depth=max_extension_depth,
                        include_modifierExtension=include_modifierExtension,
                    ),
                    True,
                ),
                # A pointer to another MolecularSequence entity as reference sequence.
                StructField(
                    "referenceSeqPointer",
                    ReferenceSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension,
                        extension_fields=extension_fields,
                        extension_depth=extension_depth + 1,
                        max_extension_depth=max_extension_depth,
                        include_modifierExtension=include_modifierExtension,
                    ),
                    True,
                ),
                # A string like "ACGT".
                StructField("referenceSeqString", StringType(), True),
                # An absolute reference to a strand. The Watson strand is the strand whose
                # 5'-end is on the short arm of the chromosome, and the Crick strand as the one
                # whose 5'-end is on the long arm.
                StructField("strand", StringType(), True),
                # Start position of the window on the reference sequence. If the coordinate
                # system is either 0-based or 1-based, then start position is inclusive.
                StructField(
                    "windowStart",
                    integerSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension,
                        extension_fields=extension_fields,
                        extension_depth=extension_depth + 1,
                        max_extension_depth=max_extension_depth,
                        include_modifierExtension=include_modifierExtension,
                    ),
                    True,
                ),
                # End position of the window on the reference sequence. If the coordinate system
                # is 0-based then end is exclusive and does not include the last position. If
                # the coordinate system is 1-base, then end is inclusive and includes the last
                # position.
                StructField(
                    "windowEnd",
                    integerSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension,
                        extension_fields=extension_fields,
                        extension_depth=extension_depth + 1,
                        max_extension_depth=max_extension_depth,
                        include_modifierExtension=include_modifierExtension,
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

        if not include_modifierExtension:
            schema.fields = [
                c
                if c.name != "modifierExtension"
                else StructField("modifierExtension", StringType(), True)
                for c in schema.fields
            ]

        return schema
