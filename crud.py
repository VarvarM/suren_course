import asyncio

from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from core.models import db_helper, User, Profile, Post, Order, Product, OrderProductAssociation


async def create_user(session: AsyncSession, username: str) -> User:
    user = User(username=username)
    session.add(user)
    await session.commit()
    return user


async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
    stmt = select(User).where(User.username == username)
    # result: Result = await session.execute(stmt)
    # user: User | None = result.scalar_one_or_none()
    user: User | None = await session.scalar(stmt)
    print('found', user, username)
    return user


async def create_user_profile(session: AsyncSession, user_id: int, first_name: str | None = None,
                              last_name: str | None = None) -> Profile:
    profile = Profile(user_id=user_id, first_name=first_name, last_name=last_name)
    session.add(profile)
    await session.commit()
    return profile


async def show_users_with_profiles(session: AsyncSession):
    stmt = select(User).options(joinedload(User.profile)).order_by(User.id)
    # result: Result = await session.execute(stmt)
    # users = result.scalars()
    users = await session.scalars(stmt)
    for user in users:
        print(user)
        print(user.profile.first_name)


async def create_posts(session: AsyncSession, user_id: int, *posts_titles: str) -> list[Post]:
    posts = [Post(title=title, user_id=user_id) for title in posts_titles]
    session.add_all(posts)
    await session.commit()
    print(posts)
    return posts


async def get_users_with_posts(session: AsyncSession):
    stmt = select(User).options(selectinload(User.posts)).order_by(User.id)
    users = await session.scalars(stmt)
    for user in users:
        print(user, '-----------')
        for post in user.posts:
            print(post)


async def get_users_with_posts_and_profile(session: AsyncSession):
    stmt = select(User).options(joinedload(User.profile), selectinload(User.posts)).order_by(User.id)
    users = await session.scalars(stmt)  # про джоины: joinedload - к одному, selectinload - ко многим
    for user in users:
        print(user, '-----------', user.profile and user.profile.first_name)
        for post in user.posts:
            print(post)


async def get_posts_with_authors(session: AsyncSession):
    stmt = select(Post).options(joinedload(Post.user)).order_by(Post.id)
    posts = await session.scalars(stmt)
    for post in posts:
        print(post, post.user)


async def get_profiles_with_authors_with_posts(session: AsyncSession):
    stmt = select(Profile).join(Profile.user).options(joinedload(Profile.user).selectinload(User.posts)).where(
        User.username == 'john').order_by(Profile.id)
    profiles = await session.scalars(stmt)
    for profile in profiles:
        print('----------')
        print(profile.first_name, profile.user)
        print(profile.user.posts)


async def create_order(session: AsyncSession, promocode: str | None = None) -> Order:
    order = Order(promocode=promocode)
    session.add(order)
    await session.commit()
    return order


async def create_product(session: AsyncSession, name: str, description: str, price: int) -> Product:
    product = Product(name=name, description=description, price=price)
    session.add(product)
    await session.commit()
    return product


async def get_orders_with_products(session: AsyncSession) -> list[Order]:
    stmt = select(Order).options(selectinload(Order.products)).order_by(Order.id)
    orders = await session.scalars(stmt)
    return list(orders)


async def create_orders_and_products(session: AsyncSession):
    order1 = await create_order(session=session)
    order_promo = await create_order(session=session, promocode="promo")
    mouse = await create_product(session, "Mouse", "Gaming mouse", 100)
    display = await create_product(session, "Display", "Display Full HD", 520)
    keyboard = await create_product(session, "Keyboard", "Pro keyboard", 250)

    order1 = await session.scalar(select(Order).where(Order.id == order1.id).options(selectinload(Order.products)))
    order_promo = await session.scalar(select(Order).where(Order.id == order_promo.id).options(
        selectinload(Order.products)))
    order1.products.append(mouse)
    order1.products.append(keyboard)
    order_promo.products.append(keyboard)
    order_promo.products.append(display)
    await session.commit()


async def demo_get_orders_with_products_through_secondary(session: AsyncSession):
    orders = await get_orders_with_products(session)
    for order in orders:
        print(order.id, order.created_at, "products:")
        for product in order.products:  # type: Product
            print(product.id, product.name, product.price)


async def get_orders_with_products_assoc(session: AsyncSession) -> list[Order]:
    stmt = select(Order).options(
        selectinload(Order.products_details).joinedload(OrderProductAssociation.product)).order_by(Order.id)
    orders = await session.scalars(stmt)
    return list(orders)


async def demo_get_orders_with_products_with_assoc(session: AsyncSession):
    orders = await get_orders_with_products_assoc(session)
    for order in orders:
        print(order.id, order.created_at, 'products:')
        for order_product_details in order.products_details:  # type: OrderProductAssociation
            print('-', order_product_details.product.id, order_product_details.product.name,
                  order_product_details.product.price, 'qty:',
                  order_product_details.count)


async def create_gift_product_for_existing_orders(session: AsyncSession):
    orders = await get_orders_with_products_assoc(session)
    gift_product = await create_product(session=session, name='gift', price=52, description='gift for you')
    for order in orders:
        order.products_details.append(OrderProductAssociation(product=gift_product, count=1, unit_price=0))
    await session.commit()


async def main_relations(session: AsyncSession):
    await create_user(session=session, username='john')
    await create_user(session=session, username='sam')
    user_john = await get_user_by_username(session=session, username='john')
    await get_user_by_username(session=session, username='bob')
    await create_user_profile(session=session, user_id=user_john.id, first_name='John')
    await show_users_with_profiles(session=session)
    await create_posts(session, user_john.id, "firssst", "sql")
    await get_users_with_posts(session=session)
    await get_posts_with_authors(session=session)
    await get_users_with_posts_and_profile(session=session)
    await get_profiles_with_authors_with_posts(session=session)


async def demo_m2m(session: AsyncSession):
    # await create_orders_and_products(session)
    # await demo_get_orders_with_products_through_secondary(session)
    await demo_get_orders_with_products_with_assoc(session)
    # await create_gift_product_for_existing_orders(session)


async def main():
    async with db_helper.session_factory() as session:
        # await main_relations(session=session)
        await demo_m2m(session=session)


if __name__ == '__main__':
    asyncio.run(main())
