# FastAPI Template - Implementation Checklist

Use this checklist when implementing a new API based on this template.

## Initial Setup

- [ ] Clone or copy the template
- [ ] Update project name in `pyproject.toml`
- [ ] Update project name in `README.md`
- [ ] Update author information in `pyproject.toml`
- [ ] Create `.env` file from `.env.example`
- [ ] Update database credentials in `.env`
- [ ] Initialize git repository: `git init`
- [ ] Create initial commit

## Environment Setup

- [ ] Install Python 3.11+
- [ ] Install dependencies: `poetry install` or `pip install -r requirements.txt`
- [ ] Activate virtual environment: `poetry shell`
- [ ] Start database: `docker-compose up -d`
- [ ] Test database connection

## Project Configuration

- [ ] Update `api/main.py` title and description
- [ ] Configure CORS if needed (uncomment in `api/main.py`)
- [ ] Add additional environment variables to `api/configs/settings.py`
- [ ] Update database URL format if not using PostgreSQL
- [ ] Configure logging if needed

## First Entity Implementation

- [ ] Create entity folder: `api/your_entity/`
- [ ] Create `__init__.py`
- [ ] Implement `models.py` (database schema)
- [ ] Implement `schemas.py` (Pydantic validation)
- [ ] Implement `controller.py` (API endpoints)
- [ ] Import model in `alembic/env.py`
- [ ] Register router in `api/routers.py`

## Database Setup

- [ ] Generate initial migration: `alembic revision --autogenerate -m "Initial"`
- [ ] Review migration file in `alembic/versions/`
- [ ] Apply migration: `alembic upgrade head`
- [ ] Verify tables created in database
- [ ] Delete example entity if not needed

## Testing

- [ ] Start the API: `uvicorn api.main:app --reload`
- [ ] Access Swagger docs: http://localhost:8000/docs
- [ ] Test health endpoint: `GET /health`
- [ ] Test create endpoint: `POST /your-entities`
- [ ] Test list endpoint: `GET /your-entities`
- [ ] Test get by ID: `GET /your-entities/{id}`
- [ ] Test update: `PATCH /your-entities/{id}`
- [ ] Test delete: `DELETE /your-entities/{id}`
- [ ] Test error cases (404, 400, etc.)
- [ ] Test filtering and pagination

## Additional Features (Optional)

- [ ] Implement authentication (JWT, OAuth2)
- [ ] Add authorization/permissions
- [ ] Implement user management
- [ ] Add file upload functionality
- [ ] Implement search functionality
- [ ] Add caching (Redis)
- [ ] Implement background tasks (Celery)
- [ ] Add email notifications
- [ ] Implement audit logging
- [ ] Add rate limiting

## Documentation

- [ ] Update README with project-specific info
- [ ] Document environment variables
- [ ] Document API endpoints
- [ ] Add usage examples
- [ ] Create API collection (Postman/Insomnia)
- [ ] Add architecture diagrams if needed

## Code Quality

- [ ] Add type hints to all functions
- [ ] Format code: `black api/`
- [ ] Lint code: `ruff check api/`
- [ ] Add docstrings to classes and functions
- [ ] Remove unused imports
- [ ] Remove commented code

## Testing (Optional but Recommended)

- [ ] Set up pytest
- [ ] Write unit tests for models
- [ ] Write unit tests for schemas
- [ ] Write integration tests for endpoints
- [ ] Set up test database
- [ ] Add test coverage reporting
- [ ] Configure CI/CD for automated testing

## Deployment Preparation

- [ ] Create production `.env` file
- [ ] Update database URL for production
- [ ] Configure production settings
- [ ] Set up logging for production
- [ ] Create Dockerfile
- [ ] Set up reverse proxy (nginx)
- [ ] Configure SSL/TLS
- [ ] Set up monitoring
- [ ] Configure backup strategy

## Security

- [ ] Enable HTTPS only
- [ ] Implement rate limiting
- [ ] Validate all inputs
- [ ] Sanitize database queries
- [ ] Use parameterized queries (SQLAlchemy does this)
- [ ] Hash passwords (bcrypt, argon2)
- [ ] Implement CSRF protection if needed
- [ ] Set secure headers
- [ ] Regular security audits
- [ ] Keep dependencies updated

## Performance

- [ ] Add database indexes
- [ ] Implement caching
- [ ] Optimize queries (use `selectinload` for relationships)
- [ ] Add pagination to all list endpoints
- [ ] Monitor query performance
- [ ] Set up connection pooling
- [ ] Implement response compression

## Git & Version Control

- [ ] Create `.gitignore` (already included)
- [ ] Commit initial template
- [ ] Create development branch
- [ ] Set up branch protection rules
- [ ] Configure pre-commit hooks
- [ ] Add commit message conventions

## Cleanup

- [ ] Remove example entity if not needed
- [ ] Remove unused dependencies
- [ ] Remove example migration files
- [ ] Update this checklist for your project

## Launch

- [ ] Deploy to staging environment
- [ ] Run final tests
- [ ] Deploy to production
- [ ] Monitor logs and errors
- [ ] Verify all endpoints work
- [ ] Check database performance
- [ ] Monitor resource usage

## Post-Launch

- [ ] Set up monitoring and alerting
- [ ] Create backup strategy
- [ ] Document deployment process
- [ ] Train team members
- [ ] Plan for scaling
- [ ] Schedule regular updates

---

**Tips:**
- Don't try to implement everything at once
- Start with core features and iterate
- Test frequently during development
- Keep security in mind from the start
- Document as you go

**Remember:** This is a template, adapt it to your needs!
