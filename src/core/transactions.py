from sqlalchemy import and_, func, select
from sqlalchemy.orm import aliased
from database import sync_session_factory, sync_engine, Base
from models.texts import TextModel
from models.words import WordModel
from schemas.texts import TextSchema
from schemas.words import WordSchema, WordGetSchema


def create_tables():
    sync_engine.echo = False
    Base.metadata.drop_all(sync_engine)
    Base.metadata.create_all(sync_engine)
    sync_engine.echo = True
    
def insert_text(text: TextSchema) -> TextModel:
    with sync_session_factory() as session:
        text_row = TextModel(content=text.content, title=text.title)
        session.add(text_row)
        session.flush()
        session.commit()
        return text_row.id        
        
def insert_words(words: list[WordSchema], text_id: int):
    with sync_session_factory() as session:
        for word in words:
            word_row = WordModel(
                word=word.word, 
                lemma=word.lemma, 
                text_id=text_id, 
                frequency=word.frequency,
                part_of_speech=word.part_of_speech, 
                feats=word.feats
                )
            session.add(word_row)
        session.flush()
        session.commit()
        
def select_texts():
    with sync_session_factory() as session:
        query = select(TextModel)
        result = session.execute(query)
        texts = result.scalars().all()
        return texts


def select_words_from_text(text_id: int):
    '''SELECT word, lemma, text_id, part_of_speech, feats, count(*) as frequency
from words	
group by word, lemma, text_id, part_of_speech, feats'''
    with sync_session_factory() as session:
        query = (
            select(WordModel)
            .filter(WordModel.text_id==text_id)
            )
        result = session.execute(query)
        words = result.scalars().all()
        return words
    
def select_word_by_pos(pos: str, text_id: int):
    with sync_session_factory() as session:
        query = (
            select(WordModel)
            .filter(and_(
                WordModel.part_of_speech==pos,
                WordModel.text_id==text_id
                ))
            )
        result = session.execute(query)
        words = result.scalars().all()
        return words
    
def select_words_by_content(text_id: int, content: str):
    with sync_session_factory() as session:
        query = (
            select(WordModel)
            .filter(and_(
                WordModel.word.contains(content),
                WordModel.text_id==text_id
                ))
            )
        result = session.execute(query)
        words = result.scalars().all()
        return words
            
