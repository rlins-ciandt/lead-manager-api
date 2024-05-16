from sqlalchemy.ext.asyncio.session import async_session
from sqlalchemy.future import select
from sqlalchemy import delete

from models import Lead

from database.connection import async_session
from services.notification import NotificationService

class LeadService():

    async def create_lead(self, first_name: str, last_name: str, email: str, resume_file: str):

        result = await self.get_by_email(email)

        if(result):
            raise Exception('We already received your application. We will contact you soon.')
       
        async with async_session() as session:
            session.add(Lead(
                first_name=first_name,
                last_name=last_name,
                email=email,
                resume_file=resume_file,
                status='PENDING'
            ))
            await session.commit()

            # Can be asyncronous and not hold the response
            NotificationService().new_lead_notification(email)

    async def delete_lead(self, lead_id: int):
        async with async_session() as session:
            result = await session.execute(delete(Lead).where(Lead.id==lead_id))

            if result.rowcount == 0:
                raise Exception('Lead not found')
            
            await session.commit()

    async def list_leads(self, ):
        async with async_session() as session:
            result = await session.execute(select(Lead))
            return result.scalars().all()
    
    async def get_by_email(self, email):
        async with async_session() as session:
            result = await session.execute(select(Lead).where(Lead.email==email))
            lead = result.scalar()

            if(lead is None):
                return None
            
            return {
                'first_name': lead.first_name,
                'last_name': lead.last_name,
                'email': lead.email,
                'status': lead.status,
            }

    async def get_resume_by_email(self, email):
        async with async_session() as session:
            result = await session.execute(select(Lead).where(Lead.email==email))
            lead = result.scalar()

            return lead.resume_file
    
    async def mark_as_reached(self, email):
        async with async_session() as session:
            result = await session.execute(select(Lead).where(Lead.email==email))
            lead = result.scalar()

            if(lead is None):
                raise Exception('Lead not found')

            lead.status = 'REACHED'
            await session.commit()
