from dataclasses import dataclass
@dataclass
class Example:
    content: str
    embedding: np.ndarray

@pydantic_dataclass
class DocumentSerialized(Example):
    content: str
    embedding: str
    # class Config:
    #     schema_extra = {
    #         'examples': [
    #             {
    #                 'name': 'John Doe',
    #                 'age': 25,
    #             }
    #         ]
    #     }
# schema_extra = {"properties": {"embedding": {"type": "int"}}}
def schema_extra(schema: Dict[str, Any]) -> None:
    schema["properties"]["embedding"]["type"] = "int"

DocumentSerialized.__pydantic_model__.Config.schema_extra = schema_extra


#
#
# @pydantic_dataclass
# class LabelSerialized(Label):
#     document: DocumentSerialized
#     # answer: Optional[AnswerSerialized] = None
#     answer: str = None
#
# class QueryResponse(BaseModel):
#     query: str
#     # answers: List[AnswerSerialized]
#     answers: List[Any]
#     # documents: Optional[List[DocumentSerialized]]
#     documents: Optional[List[Any]]

if __name__=="__main__":
    print(DocumentSerialized.__pydantic_model__.schema_json(indent=2))