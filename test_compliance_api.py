import pytest
import json
from unittest.mock import Mock, patch, MagicMock
from compliance_api import app, get_db_connection


@pytest.fixture
def client():
    """Create a test client for the Flask application."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def mock_db_connection():
    """Create a mock database connection."""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    return mock_conn, mock_cursor


class TestKYCEndpoint:
    """Test cases for the /kyc endpoint."""
    
    @patch('compliance_api.get_db_connection')
    def test_kyc_validation_success(self, mock_get_db, client):
        """Test successful KYC validation with valid customer ID."""
        # Setup mock
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db.return_value = mock_conn
        
        # Create mock customer details
        mock_customer = MagicMock()
        mock_customer.customerId = "CUST001"
        mock_customer.name = "John Doe"
        mock_customer.dob = "1990-01-01"
        mock_customer.address = "123 Main St, City, State"
        mock_cursor.fetchone.return_value = mock_customer
        
        # Make request
        response = client.get('/kyc?customerID=CUST001')
        
        # Assertions
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert data['message'] == 'KYC validation successful'
        assert data['data']['customerId'] == 'CUST001'
        assert data['data']['name'] == 'John Doe'
        assert data['data']['dob'] == '1990-01-01'
        assert data['data']['address'] == '123 Main St, City, State'
        
        # Verify database operations
        mock_cursor.execute.assert_called_once_with(
            "SELECT * FROM CustomerDetails WHERE customerId = ?", 
            "CUST001"
        )
        mock_conn.close.assert_called_once()
    
    @patch('compliance_api.get_db_connection')
    def test_kyc_validation_customer_not_found(self, mock_get_db, client):
        """Test KYC validation when customer is not found."""
        # Setup mock
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db.return_value = mock_conn
        
        # Mock customer not found
        mock_cursor.fetchone.return_value = None
        
        # Make request
        response = client.get('/kyc?customerID=INVALID001')
        
        # Assertions
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'failure'
        assert data['message'] == 'Customer not found'
        
        # Verify database operations
        mock_cursor.execute.assert_called_once()
        mock_conn.close.assert_called_once()
    
    @patch('compliance_api.get_db_connection')
    def test_kyc_validation_no_customer_id(self, mock_get_db, client):
        """Test KYC validation when no customer ID is provided."""
        # Setup mock
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db.return_value = mock_conn
        mock_cursor.fetchone.return_value = None
        
        # Make request without customerID parameter
        response = client.get('/kyc')
        
        # Assertions
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'failure'
        assert data['message'] == 'Customer not found'
    
    @patch('compliance_api.get_db_connection')
    def test_kyc_validation_with_special_characters(self, mock_get_db, client):
        """Test KYC validation with special characters in customer ID."""
        # Setup mock
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db.return_value = mock_conn
        
        # Create mock customer details
        mock_customer = MagicMock()
        mock_customer.customerId = "CUST-001"
        mock_customer.name = "Jane O'Connor"
        mock_customer.dob = "1985-05-15"
        mock_customer.address = "456 Elm St, Apt #2B"
        mock_cursor.fetchone.return_value = mock_customer
        
        # Make request
        response = client.get('/kyc?customerID=CUST-001')
        
        # Assertions
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert data['data']['name'] == "Jane O'Connor"


class TestComplianceEndpoint:
    """Test cases for the /compliance endpoint."""
    
    @patch('compliance_api.get_db_connection')
    def test_compliance_check_success(self, mock_get_db, client):
        """Test successful compliance check with valid customer ID."""
        # Setup mock
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db.return_value = mock_conn
        
        # Create mock compliance details
        mock_compliance = MagicMock()
        mock_compliance.customerId = "CUST001"
        mock_compliance.complianceType = "AML"
        mock_cursor.fetchone.return_value = mock_compliance
        
        # Make request
        response = client.get('/compliance?customerID=CUST001')
        
        # Assertions
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert data['message'] == 'Compliance check successful'
        assert data['data']['customerId'] == 'CUST001'
        assert data['data']['complianceType'] == 'AML'
        
        # Verify database operations
        mock_cursor.execute.assert_called_once_with(
            "SELECT * FROM ComplianceDetails WHERE customerId = ?", 
            "CUST001"
        )
        mock_conn.close.assert_called_once()
    
    @patch('compliance_api.get_db_connection')
    def test_compliance_check_not_found(self, mock_get_db, client):
        """Test compliance check when details are not found."""
        # Setup mock
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db.return_value = mock_conn
        
        # Mock compliance details not found
        mock_cursor.fetchone.return_value = None
        
        # Make request
        response = client.get('/compliance?customerID=INVALID001')
        
        # Assertions
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'failure'
        assert data['message'] == 'Compliance details not found'
        
        # Verify database operations
        mock_cursor.execute.assert_called_once()
        mock_conn.close.assert_called_once()
    
    @patch('compliance_api.get_db_connection')
    def test_compliance_check_no_customer_id(self, mock_get_db, client):
        """Test compliance check when no customer ID is provided."""
        # Setup mock
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db.return_value = mock_conn
        mock_cursor.fetchone.return_value = None
        
        # Make request without customerID parameter
        response = client.get('/compliance')
        
        # Assertions
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'failure'
        assert data['message'] == 'Compliance details not found'
    
    @patch('compliance_api.get_db_connection')
    def test_compliance_check_multiple_types(self, mock_get_db, client):
        """Test compliance check with different compliance types."""
        # Setup mock
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db.return_value = mock_conn
        
        # Test different compliance types
        compliance_types = ["AML", "KYC", "FATCA", "CRS"]
        
        for comp_type in compliance_types:
            mock_compliance = MagicMock()
            mock_compliance.customerId = "CUST001"
            mock_compliance.complianceType = comp_type
            mock_cursor.fetchone.return_value = mock_compliance
            
            response = client.get('/compliance?customerID=CUST001')
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data['status'] == 'success'
            assert data['data']['complianceType'] == comp_type


class TestSwaggerEndpoint:
    """Test cases for the / (Swagger spec) endpoint."""
    
    def test_swagger_spec_returns_valid_json(self, client):
        """Test that Swagger spec endpoint returns valid JSON."""
        response = client.get('/')
        
        # Assertions
        assert response.status_code == 200
        assert response.content_type == 'application/json'
        
        # Verify JSON structure
        data = json.loads(response.data)
        assert 'openapi' in data
        assert 'info' in data
        assert 'paths' in data
    
    def test_swagger_spec_contains_kyc_endpoint(self, client):
        """Test that Swagger spec contains KYC endpoint definition."""
        response = client.get('/')
        data = json.loads(response.data)
        
        # Verify KYC endpoint exists in spec
        assert '/kyc' in data['paths']
        assert 'post' in data['paths']['/kyc']
    
    def test_swagger_spec_contains_compliance_endpoint(self, client):
        """Test that Swagger spec contains compliance endpoint definition."""
        response = client.get('/')
        data = json.loads(response.data)
        
        # Verify compliance endpoint exists in spec
        assert '/compliance' in data['paths']
        assert 'post' in data['paths']['/compliance']
    
    def test_swagger_spec_version(self, client):
        """Test that Swagger spec has correct version information."""
        response = client.get('/')
        data = json.loads(response.data)
        
        # Verify version info
        assert data['openapi'] == '3.0.0'
        assert data['info']['version'] == '1.0.0'
        assert data['info']['title'] == 'KYC and Compliance API'


class TestDatabaseConnection:
    """Test cases for database connection handling."""
    
    @patch('compliance_api.pyodbc.connect')
    def test_get_db_connection_success(self, mock_connect):
        """Test successful database connection."""
        # Setup mock
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        
        # Get connection
        conn = get_db_connection()
        
        # Assertions
        assert conn == mock_conn
        mock_connect.assert_called_once()
    
    @patch('compliance_api.get_db_connection')
    def test_database_connection_closed_after_kyc(self, mock_get_db, client):
        """Test that database connection is properly closed after KYC request."""
        # Setup mock
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db.return_value = mock_conn
        mock_cursor.fetchone.return_value = None
        
        # Make request
        client.get('/kyc?customerID=TEST')
        
        # Verify connection was closed
        mock_conn.close.assert_called_once()
    
    @patch('compliance_api.get_db_connection')
    def test_database_connection_closed_after_compliance(self, mock_get_db, client):
        """Test that database connection is properly closed after compliance request."""
        # Setup mock
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db.return_value = mock_conn
        mock_cursor.fetchone.return_value = None
        
        # Make request
        client.get('/compliance?customerID=TEST')
        
        # Verify connection was closed
        mock_conn.close.assert_called_once()


class TestErrorHandling:
    """Test cases for error handling scenarios."""
    
    @patch('compliance_api.get_db_connection')
    def test_kyc_handles_database_connection_error(self, mock_get_db, client):
        """Test KYC endpoint handling of database connection errors."""
        # Setup mock to raise exception
        mock_get_db.side_effect = Exception("Database connection failed")
        
        # Make request and expect exception
        with pytest.raises(Exception):
            client.get('/kyc?customerID=CUST001')
    
    @patch('compliance_api.get_db_connection')
    def test_compliance_handles_database_connection_error(self, mock_get_db, client):
        """Test compliance endpoint handling of database connection errors."""
        # Setup mock to raise exception
        mock_get_db.side_effect = Exception("Database connection failed")
        
        # Make request and expect exception
        with pytest.raises(Exception):
            client.get('/compliance?customerID=CUST001')


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
