# Security Policy

## 🎯 Project Purpose

TechMart Vulnerable Web Application Lab is an **intentionally vulnerable** educational platform designed for security training and research. This document outlines our security policies and responsible disclosure practices.

## ⚠️ Important Notice

**This application contains deliberate security vulnerabilities for educational purposes.**

- ✅ **Intended Use**: Security training, education, and controlled research
- ❌ **Not Intended**: Production deployment or real-world use

## 🔐 Vulnerability Scope

### Intentional Vulnerabilities

The following vulnerabilities are **intentionally included** for educational purposes:

- **SQL Injection** - Authentication bypass and data extraction
- **Cross-Site Scripting (XSS)** - Stored and reflected XSS variants
- **Cross-Site Request Forgery (CSRF)** - State-changing request forgery
- **Insecure Direct Object References (IDOR)** - Unauthorized data access
- **Business Logic Flaws** - Payment and coupon abuse vulnerabilities
- **Server-Side Template Injection (SSTI)** - Code execution via templates
- **Server-Side Request Forgery (SSRF)** - Internal network access
- **Directory Traversal** - File system access vulnerabilities
- **Command Injection** - Operating system command execution
- **Broken Authentication** - Weak authentication mechanisms
- **Insecure File Upload** - Malicious file upload capabilities
- **Information Disclosure** - Sensitive data exposure

## 🚨 Reporting Issues

### Intentional Vulnerabilities

**Do NOT report the intentional vulnerabilities listed above.** These are part of the educational design and are documented in the project materials.

### Unintended Security Issues

If you discover security issues that are **not** part of the intended educational vulnerabilities, please report them responsibly:

#### What to Report
- Infrastructure vulnerabilities in Docker setup
- Unintended information disclosure beyond the lab scope
- Issues that could affect the host system
- Vulnerabilities that could allow escape from the lab environment

#### How to Report
1. **Email**: Send details to [security@example.com] *(replace with actual contact)*
2. **GitHub Issues**: For non-critical issues, open a GitHub issue with the `security` label
3. **Direct Contact**: For critical issues, contact maintainers directly

#### Information to Include
- Description of the vulnerability
- Steps to reproduce
- Potential impact assessment
- Suggested mitigation (if any)
- Your assessment of severity

### Response Timeline
- **Acknowledgment**: Within 48 hours
- **Initial Assessment**: Within 1 week
- **Resolution Timeline**: Varies based on severity and complexity

## 🔒 Security Guidelines

### For Users/Students

1. **Isolated Environment**
   - Always run in isolated/sandboxed environments
   - Use virtual machines or containers
   - Never expose to public networks

2. **Legal Compliance**
   - Only test on systems you own or have explicit permission to test
   - Respect all applicable laws and regulations
   - Use for educational purposes only

3. **Responsible Practice**
   - Don't use techniques learned here for malicious purposes
   - Practice ethical disclosure when finding real vulnerabilities
   - Contribute back to the security community

### For Instructors/Administrators

1. **Network Isolation**
   - Deploy in isolated network segments
   - Use firewall rules to prevent external access
   - Monitor for any unexpected network activity

2. **Access Control**
   - Implement proper access controls for lab environments
   - Use strong authentication for administrative access
   - Regularly audit user access and activities

3. **Data Protection**
   - Don't use real/sensitive data in the lab
   - Regularly reset lab data and configurations
   - Ensure proper data destruction when decommissioning

## 🛡️ Security Best Practices

### Deployment Security

```bash
# Example secure deployment practices
docker run --network=none techmart-lab  # No network access
docker run --read-only techmart-lab     # Read-only filesystem
docker run --user=1000 techmart-lab     # Non-root user
```

### Host Protection

1. **System Updates**
   - Keep host systems updated
   - Use latest Docker/container runtime versions
   - Apply security patches promptly

2. **Monitoring**
   - Monitor container activity
   - Log all administrative actions
   - Alert on suspicious activities

3. **Backup and Recovery**
   - Regular backups of lab configurations
   - Documented recovery procedures
   - Test recovery processes periodically

## 📋 Security Checklist

### Before Deployment
- [ ] Reviewed network isolation settings
- [ ] Configured appropriate firewall rules
- [ ] Set up monitoring and logging
- [ ] Tested in isolated environment
- [ ] Documented security procedures

### During Use
- [ ] Monitor for unexpected behavior
- [ ] Regular security assessment of infrastructure
- [ ] User access auditing
- [ ] Incident response procedures ready

### After Use
- [ ] Proper cleanup of sensitive data
- [ ] Decommissioning procedures followed
- [ ] Security lessons learned documented
- [ ] Knowledge shared with community

## 🎓 Educational Security Resources

### Recommended Reading
- [OWASP Application Security Verification Standard](https://owasp.org/www-project-application-security-verification-standard/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [SANS Top 25 Software Errors](https://www.sans.org/top25-software-errors/)

### Training Materials
- [OWASP WebGoat](https://owasp.org/www-project-webgoat/)
- [PortSwigger Web Security Academy](https://portswigger.net/web-security)
- [SANS Security Training](https://www.sans.org/)

## 📞 Contact Information

### Security Team
- **Primary Contact**: [Maintainer Email]
- **Backup Contact**: [Secondary Email]
- **Response Time**: Within 48 hours

### Community Support
- **GitHub Issues**: For general questions and support
- **Discussions**: For community interaction and learning
- **Documentation**: Comprehensive guides and tutorials

## ⚖️ Legal Disclaimer

This project is provided for educational purposes only. Users are responsible for:

- Complying with all applicable laws and regulations
- Using the software only in authorized environments
- Not using knowledge gained for malicious purposes
- Respecting intellectual property and privacy rights

The maintainers disclaim all liability for misuse of this educational tool.

---

**Remember**: The goal of this project is to improve security knowledge and skills. Use this power responsibly to make the digital world safer for everyone.
