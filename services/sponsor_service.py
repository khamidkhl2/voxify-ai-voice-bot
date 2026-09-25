from typing import Tuple, List, Dict, Any
from aiogram import Bot
from database.db import db

class SponsorService:
    @staticmethod
    async def verify_subscriptions(bot: Bot, user_id: int) -> Tuple[bool, List[Dict[str, Any]]]:
        """
        Checks if user is subscribed to all active sponsor channels.
        Returns (is_passed, missing_sponsors).
        """
        # 1. Check if user has VIP status (bypasses all ads and sponsor gates)
        if await db.is_user_vip(user_id):
            return True, []

        active_sponsors = await db.get_active_sponsors()
        if not active_sponsors:
            return True, []

        missing = []

        for sponsor in active_sponsors:
            channel_id = sponsor["channel_id"]
            try:
                # Resolve channel id/username
                chat_id_arg = int(channel_id) if (channel_id.startswith("-") or channel_id.isdigit()) else channel_id
                member = await bot.get_chat_member(chat_id=chat_id_arg, user_id=user_id)
                
                # Check status
                if member.status in ("creator", "administrator", "member", "restricted"):
                    # Record verification into DB & update sponsor delivery quota
                    await db.record_sponsor_verification(user_id, sponsor["id"])
                else:
                    missing.append(sponsor)
            except Exception as e:
                # If bot cannot check (e.g. bot not added as admin to sponsor channel), don't block user forever
                print(f"Warning: Could not check chat member for channel {channel_id}: {e}")
                # We can either skip or include. For safety, if error is bot not admin, ignore this sponsor
                pass

        is_passed = len(missing) == 0
        return is_passed, missing

sponsor_service = SponsorService()
