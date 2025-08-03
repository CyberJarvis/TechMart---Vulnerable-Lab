# Changelog

All notable changes to TechMart Vulnerable Web Application Lab will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive documentation overhaul
- Professional project structure
- Educational security policies
- Contribution guidelines

## [1.0.0] - 2025-07-20

### Added
- Initial release of TechMart Vulnerable Web Application Lab
- Complete e-commerce platform with realistic functionality
- 12+ distinct vulnerability categories for educational purposes
- Flask-based web application with SQLite database
- Bootstrap-based responsive frontend
- Docker deployment support
- Comprehensive exploit script collection
- Automated testing suite

#### Vulnerabilities Included
- **SQL Injection** - Authentication bypass and data extraction capabilities
- **Cross-Site Scripting (XSS)** - Both stored and reflected variants
- **Cross-Site Request Forgery (CSRF)** - Password change vulnerability
- **Insecure Direct Object References (IDOR)** - Receipt access control bypass
- **Business Logic Flaws** - Coupon reuse and pricing manipulation
- **Server-Side Template Injection (SSTI)** - Code execution via Jinja2
- **Server-Side Request Forgery (SSRF)** - Internal network access
- **Directory Traversal** - File system access vulnerabilities
- **Command Injection** - Operating system command execution
- **Broken Authentication** - Weak session management
- **Insecure File Upload** - File type validation bypass
- **Information Disclosure** - Sensitive data exposure

#### Features
- **Realistic E-commerce Interface** - Professional TechMart branding
- **User Management** - Registration, authentication, and profiles
- **Product Catalog** - Electronics inventory with detailed pages
- **Shopping Cart** - Add to cart and checkout functionality
- **Order Management** - Purchase history and receipt generation
- **Comment System** - Product reviews and Q&A
- **Admin Panel** - Administrative tools and system utilities
- **File Management** - Upload and download capabilities
- **Payment Processing** - Coupon system with business logic flaws

#### Security Testing Tools
- **Exploit Scripts** - Ready-to-use Python scripts for each vulnerability
- **Test Suite** - Automated vulnerability verification
- **Documentation** - Detailed exploitation walkthroughs
- **Environment Setup** - Docker and virtual environment support

### Technical Specifications
- **Python**: 3.13 compatibility
- **Flask**: 2.3.3 web framework
- **Database**: SQLite3 for simplicity
- **Frontend**: Bootstrap 5 + Jinja2 templates
- **Dependencies**: Minimal external requirements for easy setup

### Security Features (Intentionally Vulnerable)
- **No Input Validation** - Raw SQL queries and unescaped output
- **Weak Authentication** - Simple password checking
- **Missing Authorization** - Direct object reference vulnerabilities
- **Verbose Errors** - Detailed error messages for learning
- **Debug Mode** - Enabled for educational visibility
- **Weak Cryptography** - Intentionally poor security practices

### Documentation
- **README.md** - Comprehensive setup and usage guide
- **SECURITY.md** - Security policy and responsible disclosure
- **CONTRIBUTING.md** - Contribution guidelines and standards
- **LICENSE** - Educational use license
- **Exploit Documentation** - Detailed vulnerability explanations

### Development Infrastructure
- **GitHub Actions** - Automated testing and validation
- **Docker Support** - Containerized deployment options
- **Virtual Environment** - Python dependency isolation
- **Code Quality** - Linting and formatting standards
- **Testing Framework** - Pytest-based test suite

## [0.9.0] - 2025-07-19

### Added
- Initial development version
- Core Flask application structure
- Basic vulnerability implementations
- Preliminary testing framework

### Changed
- Refined vulnerability implementations
- Improved user interface design
- Enhanced documentation structure

### Fixed
- Template rendering issues
- Database initialization problems
- Dependency conflicts

## [0.1.0] - 2025-07-15

### Added
- Project inception
- Basic Flask setup
- Initial vulnerability research
- Development environment configuration

---

## Version Numbering

This project uses [Semantic Versioning](https://semver.org/) with the following conventions:

- **Major Version (X.0.0)**: Significant architectural changes or new vulnerability categories
- **Minor Version (0.X.0)**: New features, additional vulnerabilities, or substantial improvements
- **Patch Version (0.0.X)**: Bug fixes, documentation updates, or minor enhancements

## Release Notes

### Educational Focus
Each release focuses on enhancing the educational value of the platform while maintaining realistic vulnerability implementations that mirror real-world security issues.

### Backward Compatibility
We strive to maintain backward compatibility for educational setups, though vulnerability implementations may evolve to reflect current security landscapes.

### Security Updates
While this is an intentionally vulnerable application, we do address infrastructure and deployment security issues that could affect the host system.

## Future Roadmap

### Planned Features
- Additional OWASP Top 10 vulnerabilities
- Advanced exploitation techniques
- Interactive tutorial system
- Enhanced Docker security
- CI/CD integration improvements

### Community Contributions
We welcome community contributions that enhance the educational value of this platform. See CONTRIBUTING.md for guidelines.

---

For detailed information about any release, please refer to the corresponding git tags and release notes on the project repository.
