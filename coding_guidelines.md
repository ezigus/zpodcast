# ZPodcast Coding Guidelines

This document outlines the coding standards and practices to follow when contributing to the ZPodcast project.

## Table of Contents

- [Testing Guidelines](#testing-guidelines)
  - [Mocking](#mocking)
  - [Test Organization](#test-organization)
- [Code Style](#code-style)
  - [PEP 8 Compliance](#pep-8-compliance)
  - [ZPodcast-specific Style Preferences](#zpodcast-specific-style-preferences)
- [Documentation Requirements](#documentation-requirements)
- [Validation Practices](#validation-practices)
- [API Design](#api-design)
  - [Flask URL Conventions](#flask-url-conventions)
- [API Documentation Requirements](#api-documentation-requirements)
- [Project Structure](#project-structure)
- [Contribution Workflow](#contribution-workflow)
- [Documentation Style Guide](#documentation-style-guide)

## Testing Guidelines

### Mocking

#### Prefer pytest mocker fixture over MagicMock

Use the `mocker` fixture provided by pytest-mock rather than creating `MagicMock` objects directly.

```python
def test_example(mocker):
    # Good
    mocked_function = mocker.patch('module.function')
    
    # Avoid
    # from unittest.mock import MagicMock
    # mocked_function = MagicMock()
```

#### Use patch decorators for function-scoped mocks

For mocking at the function level, use the `@patch` decorator with a clear target.

```python
@patch('zpodcast.parsers.json.open', new_callable=mock_open)
@patch('json.dump')
def test_export_function(mock_json_dump, mock_file):
    # Test implementation
```

#### Use side_effect for complex mock behaviors

When a mock needs to return different values on successive calls, use `side_effect`.

```python
mock_get_rss_metadata.side_effect = [
    {"title": "Podcast 1", "description": "Description 1"},
    {"title": "Podcast 2", "description": "Description 2"}
]
```

### Test Organization

#### Use descriptive test names

Test names should clearly describe what they're testing.

```python
def test_podcast_episodes_invalid_empty():  # Good
def test_func3():  # Avoid
```

#### Group related tests with clear comments

Use comments to organize test sections.

```python
"""
Tests for podcast title validation
"""
def test_title_valid():
    # ...
```

#### Create reusable fixtures

Use pytest fixtures for test data setup.

```python
@pytest.fixture
def test_podcast_data():
    # Setup test data
    return data
```

## Code Style

### PEP 8 Compliance

All Python code should follow [PEP 8 - Style Guide for Python Code](https://peps.python.org/pep-0008/).
Developers should refer to the official documentation for detailed guidelines.

Key aspects to emphasize in our codebase:

#### Indentation

4 spaces per indentation level, no tabs

#### Line Length

Maximum of 79 characters for code, 72 for docstrings/comments

#### Imports Organization

Group imports in the order: standard library, third-party packages, local application imports

#### Naming Conventions

- `lowercase_with_underscores` for functions, methods, variables
- `CapitalizedWords` (CamelCase) for classes
- `CAPITALIZED_WITH_UNDERSCORES` for constants

Consider using tools like `flake8` or `pylint` to verify PEP 8 compliance automatically.

### ZPodcast-specific Style Preferences

#### Blank lines in docstrings

Unlike standard PEP 8, we allow (and encourage) blank lines in docstrings for better readability. For example:

```python
def process_podcast(podcast_url):
    """
    Process a podcast from its RSS feed URL.
    
    This function downloads the podcast RSS feed, parses it,
    and extracts relevant metadata and episodes.
    
    Args:
        podcast_url: The URL of the podcast RSS feed.
        
    Returns:
        A PodcastData object containing the podcast information.
        
    Raises:
        ValueError: If the podcast URL is invalid.
    """
```

#### Use dataclasses appropriately

Build upon the existing dataclass pattern for models.

#### Handle errors explicitly

Use specific exceptions with descriptive messages.

```python
if not valid_url:
    raise ValueError("Invalid podcast URL")
```

## Documentation Requirements

### Comprehensive Method Docstrings

Every method must have a detailed docstring that includes:

- A clear description of what the method does and why
- All input parameters with their types and purpose
- Return value descriptions with type information
- Any exceptions that might be raised
- Usage examples where appropriate

```python
def get_episodes(podcast_url: str) -> List[PodcastEpisode]:
    """
    Retrieves and parses podcast episodes from an RSS feed URL.
    
    This method fetches the RSS feed content from the provided URL,
    parses it using feedparser, and converts each entry into a
    PodcastEpisode object. It handles various duration formats and
    validates required fields before creating episode objects.
    
    Args:
        podcast_url (str): The URL of the RSS feed to parse. Must be a valid
                           HTTP or HTTPS URL.
    
    Returns:
        List[PodcastEpisode]: A list of PodcastEpisode objects representing
                              each episode in the feed. Returns an empty 
                              list if the feed cannot be parsed or contains 
                              no valid episodes.
    
    Raises:
        ValueError: If the podcast_url is not a valid URL string.
    
    Example:
        >>> episodes = get_episodes("https://example.com/podcast.rss")
        >>> for episode in episodes:
        >>>     print(episode.title)
    """
```

### Class Docstrings

Each class should have a docstring that explains:

- The purpose and responsibility of the class
- Important attributes
- Usage patterns
- Any inheritance relationships worth noting

```python
class PodcastData:
    """
    Represents a podcast with its metadata and episode lists.
    
    This class encapsulates all data related to a podcast, including its
    feed information, metadata, and episodes. It handles the retrieval
    and management of episode data from RSS feeds.
    
    Attributes:
        title (str): The title of the podcast
        podcast_url (str): The URL of the podcast's RSS feed
        host (str): The name of the podcast host/author
        description (str): A description of the podcast
        episodelists (List[PodcastEpisodeList]): Lists of episodes for this podcast
        podcast_priority (int): User-defined priority ranking (0-10)
        image_url (str): URL to the podcast's cover art
    """
```

### Module-Level Docstrings

Include a docstring at the top of each module file:

```python
"""
Podcast RSS Feed Parser Module

This module provides functionality for retrieving and parsing podcast
RSS feeds. It converts feed entries into structured PodcastEpisode objects
and extracts podcast metadata.

Functions:
    get_episodes: Retrieves and parses episodes from an RSS feed
    get_rss_metadata: Extracts podcast metadata from an RSS feed
"""
```

#### Type Annotations

Use Python type hints for all function parameters and return values:

```python
def format_duration(seconds: int) -> str:
    """Formats a duration in seconds to a human-readable string."""
    # Implementation
```

#### Constants Documentation

Document constants and configuration values:

```python
# Maximum priority value for podcasts (0-10 scale)
MAX_PRIORITY = 10

# Default timeout for RSS feed requests in seconds
DEFAULT_TIMEOUT = 30
```

### Inline Comments for Complex Logic

Add detailed inline comments to explain complex or non-obvious logic:

```python
def parse_duration(duration_str: str) -> int:
    """Converts various duration string formats to seconds."""
    if not duration_str:
        return 0
        
    # Handle HH:MM:SS format
    if ":" in duration_str:
        parts = duration_str.split(":")
        
        # For MM:SS format (two parts)
        if len(parts) == 2:
            # Convert minutes and seconds to total seconds
            return (int(parts[0]) * 60) + int(parts[1])
        
        # For HH:MM:SS format (three parts)
        elif len(parts) == 3:
            # Convert hours, minutes, and seconds to total seconds
            return (int(parts[0]) * 3600) + (int(parts[1]) * 60) + int(parts[2])
    
    # Handle plain seconds as string
    # Note: This assumes a simple integer string representing seconds
    return int(duration_str)
```

Specifically comment on:

- Complex algorithms and their steps
- Business logic that implements specific requirements
- Regular expressions and what they match
- Performance optimizations
- Workarounds for known issues
- Security-related measures

```python
def get_episodes(podcast_url: str) -> List[PodcastEpisode]:
    """Retrieves and parses podcast episodes from an RSS feed URL."""
    episodes = []
    feed = feedparser.parse(podcast_url)
    
    # Skip processing if feed has parsing errors
    if feed.bozo and feed.bozo_exception:
        logger.error(f"Feed parsing error: {feed.bozo_exception}")
        return episodes
    
    for entry in feed.entries:
        try:
            # Extract the audio URL from enclosures
            # RSS feeds typically include media enclosures for the podcast audio
            audio_url = None
            if hasattr(entry, 'enclosures') and entry.enclosures:
                # Check each enclosure for media content
                # Some feeds may include multiple enclosures (audio, images, etc.)
                for enclosure in entry.enclosures:
                    if 'href' in enclosure:
                        audio_url = enclosure['href']
                        break
            
            # Skip entries without audio content
            if not audio_url:
                continue
                
            # Create the episode object with all available data
            episodes.append(PodcastEpisode(
                title=entry.title,
                audio_url=audio_url,
                description=entry.get('description', ''),
                pub_date=entry.get('published', None),
                duration=parse_duration(entry.get('itunes_duration', 0)),
                episode_number=entry.get('itunes_episode', None),
                image_url=entry.get('image', {}).get('href', None)
            ))
        except (AttributeError, KeyError, ValueError) as e:
            # Log the error but continue processing other entries
            # This ensures one bad entry doesn't prevent loading all episodes
            logger.warning(f"Error processing feed entry: {e}")
            continue
            
    return episodes
```

## Validation Practices

### Validate inputs thoroughly

All public methods should validate their inputs.

### Use appropriate error messages

Error messages should be specific to the validation problem.

### Prefer validators module

Use the `validators` package for URL and other validations.

### Gracefully handle feed parsing errors

RSS/OPML parsing should handle malformed feeds gracefully.

## API Design

### Consistent blueprint structure

Follow the established pattern for Flask blueprints.

### JSON serialization

Use to_dict/from_dict methods for consistent serialization.

### Error response format

Return structured JSON for error responses.

### Success response format

- For most success responses, return structured JSON with appropriate data.
- For 204 No Content responses (such as after successful DELETE operations), return an empty string with no content.
  This is the correct HTTP standard behavior and an exception to the JSON response pattern.

```python
# Correct for 204 No Content response
return "", 204

# Incorrect for 204 No Content response
return jsonify({"success": "Resource deleted"}), 204
```

### Flask URL Conventions

Follow Flask best practices for URL design:

#### End all endpoints with a trailing slash

All API endpoints should end with a forward slash.

```python
# Correct
@app.route('/api/podcasts/', methods=['GET'])
@app.route('/api/podcasts/<int:podcast_id>/', methods=['GET'])

# Incorrect
@app.route('/api/podcasts', methods=['GET'])
@app.route('/api/podcasts/<int:podcast_id>', methods=['GET'])
```

#### Use lowercase for URL paths

Keep all URL paths lowercase for consistency.

```python
# Correct
@app.route('/api/podcasts/', methods=['GET'])

# Incorrect
@app.route('/api/Podcasts/', methods=['GET'])
```

#### Use hyphens for multi-word resources

Use hyphens (not underscores) for multi-word resource names.

```python
# Correct
@app.route('/api/popular-podcasts/', methods=['GET'])

# Incorrect
@app.route('/api/popular_podcasts/', methods=['GET'])
```

#### Follow RESTful resource naming

Use plural nouns for collections and appropriate HTTP methods.

```python
# Collection (plural noun)
@app.route('/api/podcasts/', methods=['GET'])  # List all podcasts
@app.route('/api/podcasts/', methods=['POST'])  # Create a new podcast

# Individual resource (with ID)
@app.route('/api/podcasts/<int:podcast_id>/', methods=['GET'])  # Get a specific podcast
@app.route('/api/podcasts/<int:podcast_id>/', methods=['PUT'])  # Update a podcast
@app.route('/api/podcasts/<int:podcast_id>/', methods=['DELETE'])  # Delete a podcast
```

#### Use query parameters for filtering, sorting, and pagination

```python
# Filtering and sorting
@app.route('/api/podcasts/', methods=['GET'])
def get_podcasts():
    """Get podcasts with optional filtering and sorting"""
    # Access query parameters with request.args
    sort_by = request.args.get('sort_by', 'title')
    order = request.args.get('order', 'asc')
    category = request.args.get('category')
    
    # Implementation
```

#### Use nested routes for resource relationships

```python
# Get episodes belonging to a specific podcast
@app.route('/api/podcasts/<int:podcast_id>/episodes/', methods=['GET'])

# Add an episode to a specific playlist
@app.route('/api/playlists/<int:playlist_id>/episodes/', methods=['POST'])
```

## API Documentation Requirements

### Swagger/OpenAPI Documentation

All new API endpoints must include Swagger/OpenAPI documentation.

### Use Flask-specific decorators

Use Flask's route decorators with OpenAPI annotations:

```python
@app.route('/api/podcasts/', methods=['GET'])
@swag_from({
    'responses': {
        200: {
            'description': 'List of all podcasts',
            'schema': PodcastListSchema
        },
        500: {
            'description': 'Server error'
        }
    },
    'summary': 'Retrieves all podcasts',
    'tags': ['podcasts']
})
def get_podcasts():
    """
    Returns a list of all podcasts in the system.
    
    This endpoint retrieves all podcasts with their basic metadata,
    excluding episodes to keep response size manageable.
    """
    # Implementation
```

### Define schemas

Create Swagger/OpenAPI schemas for all response and request objects:

```python
PodcastSchema = {
    'type': 'object',
    'properties': {
        'id': {'type': 'integer', 'description': 'Unique podcast identifier'},
        'title': {'type': 'string', 'description': 'Podcast title'},
        'podcast_url': {'type': 'string', 'description': 'RSS feed URL'},
        'host': {'type': 'string', 'description': 'Podcast host/author'},
        'description': {'type': 'string', 'description': 'Podcast description'},
        'podcast_priority': {'type': 'integer', 'description': 'User priority (0-10)'},
        'image_url': {'type': 'string', 'description': 'Podcast cover art URL'}
    },
    'required': ['title', 'podcast_url']
}

PodcastListSchema = {
    'type': 'array',
    'items': PodcastSchema
}
```

### Document all parameters

Include documentation for path, query, and body parameters:

```python
@app.route('/api/podcasts/<int:podcast_id>', methods=['GET'])
@swag_from({
    'parameters': [
        {
            'name': 'podcast_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'Unique identifier of the podcast'
        }
    ],
    'responses': {
        200: {
            'description': 'Podcast details',
            'schema': PodcastSchema
        },
        404: {
            'description': 'Podcast not found'
        }
    },
    'summary': 'Get podcast by ID',
    'tags': ['podcasts']
})
def get_podcast(podcast_id):
    # Implementation
```

### Group endpoints logically

Use tags to group related endpoints:

```python
# Tags for all podcast-related endpoints
'tags': ['podcasts']

# Tags for all playlist-related endpoints
'tags': ['playlists']
```

### Document error responses

Include documentation for all possible error responses:

```python
'responses': {
    200: {'description': 'Success'},
    400: {'description': 'Bad request - Invalid input data'},
    404: {'description': 'Resource not found'},
    500: {'description': 'Server error'}
}
```

### Generate Swagger UI

Ensure the API provides a Swagger UI endpoint for interactive documentation:

```python
# In app initialization
swagger = Swagger(app, template=swagger_template)
```

### Update API documentation when changing endpoints

When modifying existing endpoints, update the Swagger documentation to reflect the changes.

### Versioning

Include API version information in the documentation:

```python
swagger_template = {
    'info': {
        'title': 'ZPodcast API',
        'description': 'API for managing podcasts and playlists',
        'version': '1.0.0'
    }
}
```

## Project Structure

The ZPodcast project follows a modular structure with clear separation of concerns.
Understanding this structure is essential for proper contribution.

### Core Module Organization

The core functionality is organized as follows:

```text
zpodcast/
├── core/           # Core domain models and business logic
├── parsers/        # Parsing modules for different formats (RSS, JSON, OPML)
├── api/            # API interfaces and route definitions
│   └── blueprints/ # Flask blueprints organized by resource
└── utils/          # Utility and helper functions
```

#### Module Responsibilities

- **core/**: Contains all domain entities and business logic
  - Podcast and episode data models
  - Collection management (playlists, podcast lists)
  - Core operations on domain entities

- **parsers/**: Handles external data parsing and serialization
  - RSS feed parsing (`rss.py`)
  - JSON import/export (`json.py`)
  - OPML import/export (`opml.py`)

- **api/**: Web API implementation
  - Flask application setup (`app.py`)
  - API routes definition (`routes.py`)
  - Resource-specific blueprints in `blueprints/`

- **utils/**: Shared utilities and helper functions
  - Common helper functions (`helpers.py`)
  - Sorting and filtering utilities (`sort.py`)

#### File Naming Conventions

- Use singular names for modules defining a single primary class (`podcast.py`, `episode.py`)
- Use plural names for modules managing collections (`podcasts.py`, `playlists.py`)
- Test files should mirror the structure of the main package with a `test_` prefix

#### Add New Functionality in the Right Place

When adding new features:

1. Core business logic belongs in the `core/` package
2. New data formats should be added as new modules in `parsers/`
3. New API endpoints should be organized into appropriate blueprints
4. Cross-cutting utilities should go in `utils/`

## Contribution Workflow

### Getting Started

1. **Fork and Clone**: Fork the ZPodcast repository and clone it locally
2. **Set Up Environment**: Install dependencies with `pip install -r requirements.txt`
3. **Create Branch**: Create a feature branch with a descriptive name:

```bash
git checkout -b feature/add-search-capability
```

### Development Process

#### 1. Test-Driven Development

Write tests first, then implement the feature to satisfy the tests:

```bash
# Run specific tests
pytest tests/core/test_podcast.py -v

# Run all tests
pytest
```

#### 2. Code Formatting

Format your code before committing:

```bash
# Check PEP 8 compliance
flake8 zpodcast

# Format code with Black
black zpodcast tests
```

#### 3. Type Checking

Ensure proper type annotations and run mypy:

```bash
mypy zpodcast
```

### Pull Request Process

1. **Update Documentation**: Ensure all new code is documented
2. **Run Tests**: Make sure all tests pass locally
3. **Submit PR**: Create a pull request with a clear description of changes
4. **Code Review**: Address any feedback from code reviews
5. **Merge**: Once approved, your PR will be merged

### Release Process

Releases follow semantic versioning:

- **MAJOR**: Incompatible API changes
- **MINOR**: New functionality in a backward-compatible manner
- **PATCH**: Backward-compatible bug fixes

Version numbers are managed in `setup.cfg` and should be updated as part of the release process.

## Documentation Style Guide

The ZPodcast project follows standard markdown formatting rules to ensure consistent documentation.
All markdown files (`.md`) should adhere to the following guidelines.

### Markdown Linting Standards

#### File Structure

- Use a single `#` (H1) at the top of the document as the title
- Use sequential header levels without skipping (H1 -> H2 -> H3, not H1 -> H3)
- Include a blank line before and after headers
- Include a table of contents for documents longer than 100 lines

#### Text Formatting

- Write one sentence per line for better git diffs
- Limit line length to 120 characters
- Use blank lines between paragraphs
- Use **italics** for emphasis, not underscores
- Use **bold** for strong emphasis
- Do not use ALL CAPS for emphasis

#### Lists

- Use `-` for unordered lists (not `*`)
- Use `1.` for ordered lists
- Use consistent indentation (2 spaces) for nested lists
- Include a blank line before and after lists
- Do not include blank lines between list items

```markdown
- First item
- Second item
  - Nested item
  - Another nested item
- Third item
```

#### Code Blocks

- Always specify the language for syntax highlighting
- Use triple backticks for code blocks
- Use single backticks for inline code

Correct example:

```python
def example():
    return True
```

Incorrect example:

```python
def example():
    return True
```

#### Links and References

- Use reference-style links for better readability
- Use descriptive link texts (avoid "click here" or "this link")

```markdown
[ZPodcast API Documentation][api-docs]

[api-docs]: https://zpodcast.example.com/docs
```

#### Images

- Include alt text for all images
- Use a consistent naming convention for image files

```markdown
![ZPodcast Logo](images/zpodcast-logo.png)
```

#### Tables

- Use tables for structured data
- Include a header row
- Align columns for better readability

```markdown
| Podcast Name | Host         | Episodes |
|-------------|--------------|----------|
| TechTalk    | John Smith   | 42       |
| CodeCast    | Jane Doe     | 28       |
```

### Markdown Linting Tools

Install and use markdown linting tools to automatically check for style consistency:

```bash
# Install markdownlint CLI
npm install -g markdownlint-cli

# Check a specific file
markdownlint coding_guidelines.md

# Check all markdown files
markdownlint "**/*.md"
```

We recommend configuring your editor to use markdownlint for real-time validation.

### Documentation File Organization

- Place general project documentation in the root directory
- Place API documentation in the `docs/api` directory
- Place user guides in the `docs/guides` directory
- Name files with lowercase kebab-case (e.g., `api-reference.md`)

### README Standards

Every module should have a README.md file that includes:

1. Module purpose and responsibility
2. Installation instructions (if applicable)
3. Usage examples
4. Links to related documentation
