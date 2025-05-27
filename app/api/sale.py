from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, extract, and_, cast, String 
from datetime import date, timedelta
from typing import List, Optional
from ..schemas.sale import SaleCreate, Sale, SaleAnalysis, PeriodData, RevenueComparison
from ..models.sale import Sale as SaleModel
from ..models.product import Product as ProductModel
from ..db.session import get_db


router = APIRouter()

@router.post("/sales/", response_model=Sale)
def create_sale(sale: SaleCreate, db: Session = Depends(get_db)):
    db_sale = SaleModel(**sale.dict())
    db.add(db_sale)
    db.commit()
    db.refresh(db_sale)
    return db_sale

@router.get("/sales/{sale_id}", response_model=Sale)
def read_sale(sale_id: int, db: Session = Depends(get_db)):
    db_sale = db.query(SaleModel).filter(SaleModel.id == sale_id).first()
    if db_sale is None:
        raise HTTPException(status_code=404, detail="Sale not found")
    return db_sale

@router.get("/sales/", response_model=List[Sale])
def read_sales(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    product_id: Optional[int] = None,
    category: Optional[str] = None
):
    query = db.query(SaleModel)

    if start_date and end_date:
        query = query.filter(and_(SaleModel.sale_date >= start_date, SaleModel.sale_date <= end_date))
    elif start_date:
        query = query.filter(SaleModel.sale_date >= start_date)
    elif end_date:
        query = query.filter(SaleModel.sale_date <= end_date)

    if product_id:
        query = query.filter(SaleModel.product_id == product_id)

    if category:
        query = query.join(SaleModel.product).filter(ProductModel.category == category)

    return query.offset(skip).limit(limit).all()


@router.get("/sales/analysis/daily", response_model=List[SaleAnalysis])
def get_daily_sales_analysis(
    db: Session = Depends(get_db),
    start_date: date = Query(date.today() - timedelta(days=30)),
    end_date: date = Query(date.today())
):
    daily_sales = db.query(
        func.date(SaleModel.sale_date).label("date"),
        func.sum(SaleModel.revenue).label("total_revenue"),
        func.count(SaleModel.id).label("total_sales")
    ).filter(
        and_(
            SaleModel.sale_date >= start_date,
            SaleModel.sale_date <= end_date
        )
    ).group_by(
        func.date(SaleModel.sale_date)
    ).all()

    return [
        SaleAnalysis(
            date=row.date.isoformat(),  # Convert date to string
            total_revenue=float(row.total_revenue) if row.total_revenue else 0,
            total_sales=row.total_sales
        )
        for row in daily_sales
    ]


@router.get("/sales/analysis/weekly", response_model=List[SaleAnalysis])
def get_weekly_sales_analysis(
    db: Session = Depends(get_db),
    start_date: date = Query(date.today() - timedelta(days=30)),
    end_date: date = Query(date.today())
):
    weekly_sales = db.query(
        func.concat(
            func.extract('year', SaleModel.sale_date).cast(String),
            '-W',
            func.extract('week', SaleModel.sale_date).cast(String)
        ).label("week"),
        func.sum(SaleModel.revenue).label("total_revenue"),
        func.count(SaleModel.id).label("total_sales")
    ).filter(
        and_(
            SaleModel.sale_date >= start_date,
            SaleModel.sale_date <= end_date
        )
    ).group_by(
        func.extract('year', SaleModel.sale_date),
        func.extract('week', SaleModel.sale_date)
    ).all()

    return [
        SaleAnalysis(
            week=row.week,
            total_revenue=float(row.total_revenue) if row.total_revenue else 0,
            total_sales=row.total_sales
        )
        for row in weekly_sales
    ]


@router.get("/sales/analysis/monthly", response_model=List[SaleAnalysis])
def get_monthly_sales_analysis(
    db: Session = Depends(get_db),
    start_date: date = Query(date.today() - timedelta(days=30)),
    end_date: date = Query(date.today())
):
    monthly_sales = db.query(
        func.concat(
            cast(func.extract('year', SaleModel.sale_date), String),
            '-',
            cast(func.extract('month', SaleModel.sale_date), String)
        ).label("month"),
        func.sum(SaleModel.revenue).label("total_revenue"),
        func.count(SaleModel.id).label("total_sales")
    ).filter(
        and_(
            SaleModel.sale_date >= start_date,
            SaleModel.sale_date <= end_date
        )
    ).group_by(
        func.extract('year', SaleModel.sale_date),
        func.extract('month', SaleModel.sale_date)
    ).order_by(
        func.extract('year', SaleModel.sale_date),
        func.extract('month', SaleModel.sale_date)
    ).all()

    return [
        SaleAnalysis(
            month=row.month,
            total_revenue=float(row.total_revenue) if row.total_revenue else 0,
            total_sales=row.total_sales
        )
        for row in monthly_sales
    ]


@router.get("/sales/analysis/annual", response_model=List[SaleAnalysis])
def get_annual_sales_analysis(
    db: Session = Depends(get_db),
    start_date: date = Query(date.today() - timedelta(days=365)),
    end_date: date = Query(date.today())
):
    annual_sales = db.query(
        cast(func.extract('year', SaleModel.sale_date), String).label("year"),
        func.sum(SaleModel.revenue).label("total_revenue"),
        func.count(SaleModel.id).label("total_sales")
    ).filter(
        and_(
            SaleModel.sale_date >= start_date,
            SaleModel.sale_date <= end_date
        )
    ).group_by(
        func.extract('year', SaleModel.sale_date)
    ).order_by(
        func.extract('year', SaleModel.sale_date)
    ).all()

    return [
        SaleAnalysis(
            year=row.year,
            total_revenue=float(row.total_revenue) if row.total_revenue else 0,
            total_sales=row.total_sales
        )
        for row in annual_sales
    ]

@router.get("/sales/analysis/compare", response_model=RevenueComparison)
def compare_sales_analysis(
    db: Session = Depends(get_db),
    period1_start: date = Query(date.today() - timedelta(days=60)),
    period1_end: date = Query(date.today() - timedelta(days=30)),
    period2_start: date = Query(date.today() - timedelta(days=30)),
    period2_end: date = Query(date.today())
):
    period1_sales = db.query(
        func.sum(SaleModel.revenue).label("total_revenue"),
        func.count(SaleModel.id).label("total_sales")
    ).filter(
        and_(
            SaleModel.sale_date >= period1_start,
            SaleModel.sale_date <= period1_end
        )
    ).first()

    period2_sales = db.query(
        func.sum(SaleModel.revenue).label("total_revenue"),
        func.count(SaleModel.id).label("total_sales")
    ).filter(
        and_(
            SaleModel.sale_date >= period2_start,
            SaleModel.sale_date <= period2_end
        )
    ).first()

    return RevenueComparison(
        period1=PeriodData(
            total_revenue=float(period1_sales.total_revenue) if period1_sales and period1_sales.total_revenue else 0,
            total_sales=period1_sales.total_sales if period1_sales else 0
        ),
        period2=PeriodData(
            total_revenue=float(period2_sales.total_revenue) if period2_sales and period2_sales.total_revenue else 0,
            total_sales=period2_sales.total_sales if period2_sales else 0
        ),
        comparison={
            "revenue_difference": (float(period1_sales.total_revenue) if period1_sales and period1_sales.total_revenue else 0) -
                          (float(period2_sales.total_revenue) if period2_sales and period2_sales.total_revenue else 0),
            "sales_difference": (period1_sales.total_sales if period1_sales else 0) -
                              (period2_sales.total_sales if period2_sales else 0)
        }
    )


@router.get("/sales/analysis/by-category", response_model=List[SaleAnalysis])
def get_sales_by_category(
    db: Session = Depends(get_db),
    start_date: date = Query(date.today() - timedelta(days=30)),
    end_date: date = Query(date.today())
):
    category_sales = db.query(
        ProductModel.category.label("category"),
        func.sum(SaleModel.revenue).label("total_revenue"),
        func.count(SaleModel.id).label("total_sales")
    ).join(
        ProductModel, SaleModel.product_id == ProductModel.id
    ).filter(
        and_(
            SaleModel.sale_date >= start_date,
            SaleModel.sale_date <= end_date
        )
    ).group_by(
        ProductModel.category
    ).all()

    return [
        SaleAnalysis(
            category=row.category,
            total_revenue=float(row.total_revenue) if row.total_revenue else 0,
            total_sales=row.total_sales
        )
        for row in category_sales
    ]
