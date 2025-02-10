"""
测试配置文件
"""
import os
import pytest
import shutil

@pytest.fixture(scope="session", autouse=True)
def setup_test_env():
    """设置测试环境"""
    # 创建测试数据目录
    test_data_dir = 'tests/test_data'
    os.makedirs(test_data_dir, exist_ok=True)
    
    yield
    
    # 清理测试数据
    if os.path.exists(test_data_dir):
        shutil.rmtree(test_data_dir)

@pytest.fixture(scope="session")
def test_html_samples():
    """提供测试用HTML样本"""
    return {
        'list_page': '''
        <div class="leftContent">
            <h2 class="total">共找到<span>2</span>套北京二手房</h2>
            <div class="info clear">
                <div class="title">
                    <a href="/ershoufang/123456.html" class="title">测试房源1</a>
                </div>
                <div class="priceInfo">
                    <div class="totalPrice"><span>500</span>万</div>
                    <div class="unitPrice"><span>50000</span>元/平米</div>
                </div>
                <div class="houseInfo">2室1厅 | 89.12平米 | 南 | 精装</div>
                <div class="positionInfo">中楼层(共18层) 2010年建</div>
            </div>
        </div>
        ''',
        'detail_page': '''
        <div class="house-title">
            <h1 class="main">测试房源详情</h1>
        </div>
        <div class="price">
            <span class="total">500</span>万
            <div class="text">
                <span class="unitPriceValue">50000</span>元/平米
            </div>
        </div>
        '''
    }

@pytest.fixture(scope="session")
def test_data_samples():
    """提供测试用数据样本"""
    return {
        'house_item': {
            'house_id': '123456',
            'title': '测试房源',
            'total_price': '500万',
            'unit_price': '50000元/平米',
            'community': '测试小区',
            'area': '朝阳区 望京',
            'house_type': '2室1厅',
            'floor': '中楼层(共18层)',
            'orientation': '南',
            'decoration': '精装',
            'has_elevator': '有',
            'build_year': '2010年建'
        }
    }
