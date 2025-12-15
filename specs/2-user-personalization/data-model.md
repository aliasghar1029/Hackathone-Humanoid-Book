# Data Model: Personalized Learning Platform

## Entity: UserProfile

### Overview
Stores user authentication data and personalization preferences captured during signup.

### Fields
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| userId | String | Required, Unique | Unique identifier from Better-Auth.com |
| background | String | Required, Enum | User's technical background: "software-focused", "hardware-focused", "mixed" |
| preferences | JSON | Optional | User's personalization and UI preferences |
| createdAt | DateTime | Required | Timestamp of account creation |
| lastLogin | DateTime | Optional | Timestamp of last login |
| isActive | Boolean | Required, Default: true | Account status flag |

### Relationships
- None (standalone entity)

### Validation Rules
- `userId` must be a valid Better-Auth.com user ID
- `background` must be one of the predefined values
- `preferences` must be valid JSON if provided
- `createdAt` must be in the past
- `isActive` is true by default

### State Transitions
- `isActive`: `true` → `false` (after 1 year of inactivity)

## Entity: PersonalizationRule

### Overview
Defines content modification rules based on user background preferences for personalized learning experience.

### Fields
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| ruleId | UUID | Required, Unique | Unique identifier for the rule |
| contentSelector | String | Required | CSS selector or content identifier to target |
| modificationType | String | Required, Enum | Type of modification: "highlight", "emphasize", "simplify", "expand", "add-context" |
| targetAudience | String | Required, Enum | Audience for this rule: "software-focused", "hardware-focused", "mixed" |
| modificationContent | String | Required | Content to replace or add |
| priority | Integer | Required, Positive | Order in which rules are applied |
| isActive | Boolean | Required, Default: true | Whether this rule is currently active |
| createdAt | DateTime | Required | When the rule was created |

### Relationships
- None (standalone entity)

### Validation Rules
- `contentSelector` must be a valid CSS selector or content identifier
- `modificationType` must be one of the predefined values
- `targetAudience` must be one of the predefined values
- `priority` must be a positive integer
- `isActive` is true by default

### State Transitions
- `isActive`: `true` → `false` (when rule is deactivated)

## Entity: TranslationCache

### Overview
Caches translated content to improve performance and reduce API costs for Urdu translation feature.

### Fields
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| cacheId | UUID | Required, Unique | Unique identifier for the cached translation |
| originalContentHash | String | Required, Unique | SHA-256 hash of original content |
| originalContent | String | Required | Original English content |
| translatedContent | String | Required | Urdu translation of the content |
| language | String | Required, Default: "ur" | Target language code (currently "ur" for Urdu) |
| context | String | Optional | Context provided during translation for better accuracy |
| createdAt | DateTime | Required | When the translation was cached |
| expiresAt | DateTime | Required | When the cache entry expires |
| hitCount | Integer | Required, Default: 0 | Number of times this translation was used |

### Relationships
- None (standalone entity)

### Validation Rules
- `originalContentHash` must be unique
- `language` must be a valid language code
- `expiresAt` must be in the future
- `hitCount` must be non-negative
- `originalContent` and `translatedContent` must not be empty

### State Transitions
- None (expiration handled by TTL)

## Entity: SubagentConfiguration

### Overview
Configuration for Claude Code Subagents that handle personalization and translation logic.

### Fields
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| configId | UUID | Required, Unique | Unique identifier for the configuration |
| agentName | String | Required | Name of the subagent |
| agentType | String | Required, Enum | Type of agent: "personalization", "translation", "content-modification" |
| configuration | JSON | Required | Parameters and settings for the agent |
| isActive | Boolean | Required, Default: true | Whether the agent is currently active |
| createdAt | DateTime | Required | When the configuration was created |
| updatedAt | DateTime | Optional | When the configuration was last updated |

### Relationships
- None (standalone entity)

### Validation Rules
- `agentType` must be one of the predefined values
- `configuration` must be valid JSON
- `isActive` is true by default
- `updatedAt` must be after `createdAt` if provided

### State Transitions
- `isActive`: `true` → `false` (when agent is disabled)

## Entity: UserSession

### Overview
Temporary session data for authenticated users, stored in browser storage.

### Fields
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| sessionId | String | Required | Session identifier from Better-Auth |
| userId | String | Required | Reference to UserProfile.userId |
| background | String | Required | User's technical background (cached for performance) |
| personalizationEnabled | Boolean | Required, Default: false | Whether personalization is currently active |
| translationEnabled | Boolean | Required, Default: false | Whether translation is currently active |
| targetLanguage | String | Optional, Default: "en" | Current translation language |
| preferences | JSON | Optional | Temporary user preferences for current session |

### Relationships
- References: UserProfile.userId

### Validation Rules
- `userId` must reference an existing UserProfile
- `background` must match the value in UserProfile
- `targetLanguage` must be a valid language code if provided
- `preferences` must be valid JSON if provided

### State Transitions
- Session expires after configured timeout period

## Entity: ContentMetadata

### Overview
Metadata for textbook content to support personalization and translation features.

### Fields
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| contentId | String | Required, Unique | Unique identifier for the content piece |
| contentType | String | Required, Enum | Type of content: "chapter", "section", "paragraph", "code-block", "diagram" |
| originalText | String | Required | Original English text content |
| technicalTerms | Array of String | Optional | Technical terms in the content for translation assistance |
| difficultyLevel | String | Optional, Enum | Difficulty: "beginner", "intermediate", "advanced" |
| domainTags | Array of String | Optional | Domain tags: "software", "hardware", "theory", "practice" |
| personalizationHooks | Array of String | Optional | CSS selectors where personalization can be applied |
| lastModified | DateTime | Required | When the content was last updated |

### Relationships
- None (standalone entity)

### Validation Rules
- `contentType` must be one of the predefined values
- `difficultyLevel` must be one of the predefined values if provided
- `domainTags` values must be from predefined set if provided
- `technicalTerms` must be non-empty strings if provided

### State Transitions
- None (content updates create new versions)