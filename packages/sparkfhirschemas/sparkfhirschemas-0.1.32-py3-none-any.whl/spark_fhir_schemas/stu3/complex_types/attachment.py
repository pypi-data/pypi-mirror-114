from typing import Union, List, Optional

from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    ArrayType,
    IntegerType,
    DataType,
)


# This file is auto-generated by generate_schema so do not edit manually
# noinspection PyPep8Naming
class AttachmentSchema:
    """
    For referring to data content defined in other formats.
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
        For referring to data content defined in other formats.


        id: unique id for the element within a resource (for internal references). This
            may be any string value that does not contain spaces.

        extension: May be used to represent additional information that is not part of the basic
            definition of the element. In order to make the use of extensions safe and
            manageable, there is a strict set of governance  applied to the definition and
            use of extensions. Though any implementer is allowed to define an extension,
            there is a set of requirements that SHALL be met as part of the definition of
            the extension.

        contentType: Identifies the type of the data in the attachment and allows a method to be
            chosen to interpret or render the data. Includes mime type parameters such as
            charset where appropriate.

        language: The human language of the content. The value can be any valid value according
            to BCP 47.

        data: The actual data of the attachment - a sequence of bytes. In XML, represented
            using base64.

        url: An alternative location where the data can be accessed.

        size: The number of bytes of data that make up this attachment (before base64
            encoding, if that is done).

        hash: The calculated hash of the data using SHA-1. Represented using base64.

        title: A label or set of text to display in place of the data.

        creation: The date that the attachment was first created.

        """
        from spark_fhir_schemas.stu3.complex_types.extension import ExtensionSchema

        if (
            max_recursion_limit
            and nesting_list.count("Attachment") >= max_recursion_limit
        ) or (max_nesting_depth and nesting_depth >= max_nesting_depth):
            return StructType([StructField("id", StringType(), True)])
        # add my name to recursion list for later
        my_nesting_list: List[str] = nesting_list + ["Attachment"]
        schema = StructType(
            [
                # unique id for the element within a resource (for internal references). This
                # may be any string value that does not contain spaces.
                StructField("id", StringType(), True),
                # May be used to represent additional information that is not part of the basic
                # definition of the element. In order to make the use of extensions safe and
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
                # Identifies the type of the data in the attachment and allows a method to be
                # chosen to interpret or render the data. Includes mime type parameters such as
                # charset where appropriate.
                StructField("contentType", StringType(), True),
                # The human language of the content. The value can be any valid value according
                # to BCP 47.
                StructField("language", StringType(), True),
                # The actual data of the attachment - a sequence of bytes. In XML, represented
                # using base64.
                StructField("data", StringType(), True),
                # An alternative location where the data can be accessed.
                StructField("url", StringType(), True),
                # The number of bytes of data that make up this attachment (before base64
                # encoding, if that is done).
                StructField("size", IntegerType(), True),
                # The calculated hash of the data using SHA-1. Represented using base64.
                StructField("hash", StringType(), True),
                # A label or set of text to display in place of the data.
                StructField("title", StringType(), True),
                # The date that the attachment was first created.
                StructField("creation", StringType(), True),
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
