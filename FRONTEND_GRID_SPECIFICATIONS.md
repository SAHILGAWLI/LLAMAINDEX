# 🎯 Legal Dashboard Frontend Grid Specifications

## 📋 Overview
The legal dashboard consists of **5 main grids** that populate hierarchically, providing comprehensive case analysis for police officers and legal professionals.

## 🏗️ Grid Layout Structure

### **Main Dashboard Layout: 5-Grid System**

```
┌─────────────────────────────────────────────────────────────┐
│                    CASE HEADER                              │
│  Case ID: CASE-2024-001 | Status: Active | Officer: John   │
└─────────────────────────────────────────────────────────────┘

┌─────────────────┬─────────────────┬─────────────────────────┐
│                 │                 │                         │
│   GRID 1        │   GRID 2        │      GRID 3             │
│  COMPLIANCE     │    LAWS         │    DOCUMENTS            │
│                 │                 │                         │
└─────────────────┴─────────────────┴─────────────────────────┘

┌─────────────────────────────────┬───────────────────────────┐
│                                 │                           │
│           GRID 4                │        GRID 5             │
│          CASES                  │     LIVE CASES            │
│                                 │                           │
└─────────────────────────────────┴───────────────────────────┘
```

---

## 🔧 Grid 1: Compliance Checklist

### **API Endpoint**: `POST /dashboard/populate-hierarchical`
### **Response Field**: `grid_1_compliance`

### **UI Components**:
```javascript
{
  "checklist_items": [
    {
      "item": "Ensure timely documentation of surgical procedure",
      "status": "not_started" | "in_progress" | "completed",
      "priority": "high" | "medium" | "low",
      "due_date": "2024-01-15" | null,
      "notes": "Additional notes" | null
    }
  ],
  "progress": "3/5 Complete",
  "percentage": 60,
  "overall_status": "In Progress" | "Completed" | "Overdue",
  "recommendations": "Focus on high-priority items first"
}
```

### **Frontend Implementation**:
- **Progress Bar**: Visual progress indicator (0-100%)
- **Checklist Items**: Interactive checkboxes with status colors
- **Priority Badges**: High (Red), Medium (Yellow), Low (Green)
- **Status Icons**: ✅ Completed, 🔄 In Progress, ⏳ Not Started
- **Due Date Alerts**: Red for overdue, yellow for due soon

---

## 📚 Grid 2: Laws Reference

### **API Endpoint**: `POST /dashboard/populate-hierarchical`
### **Response Field**: `grid_2_laws`

### **UI Components**:
```javascript
{
  "laws": [
    {
      "section": "302",
      "title": "Punishment for murder",
      "severity": "High" | "Medium" | "Low",
      "relevance_score": 0.95,
      "description": "Whoever commits murder shall be punished...",
      "penalties": "Death or life imprisonment"
    }
  ],
  "total_found": 5,
  "context_summary": "Found 5 relevant law sections for medical malpractice",
  "legal_analysis": "Detailed legal analysis text..."
}
```

### **Frontend Implementation**:
- **Law Cards**: Each law as a card with section number prominently displayed
- **Severity Indicators**: High (Red badge), Medium (Orange), Low (Green)
- **Relevance Score**: Progress bar or star rating (0-1 scale)
- **Expandable Details**: Click to expand full description and penalties
- **Search/Filter**: Filter by severity, relevance score, or section number

---

## 📄 Grid 3: Documents

### **API Endpoint**: `POST /dashboard/populate-hierarchical`
### **Response Field**: `grid_3_documents`

### **UI Components**:
```javascript
{
  "documents": [
    {
      "id": "doc_CASE-2024-001_001",
      "name": "Expert Report - High Priority",
      "type": "legal_document" | "evidence" | "witness_statement",
      "priority": "high" | "medium" | "low",
      "summary": "Document summary text",
      "upload_date": "2025-07-23",
      "file_size": "2.5 MB",
      "status": "processed" | "pending" | "error"
    }
  ],
  "total_documents": 12,
  "categories": {
    "legal_document": 8,
    "evidence": 3,
    "witness_statement": 1
  },
  "ai_insights": "Key insights from document analysis"
}
```

### **Frontend Implementation**:
- **Document List**: Table or card view with sorting capabilities
- **Type Icons**: 📄 Legal Doc, 🔍 Evidence, 👥 Witness Statement
- **Priority Badges**: Color-coded priority indicators
- **Status Indicators**: ✅ Processed, ⏳ Pending, ❌ Error
- **Category Filters**: Filter by document type
- **Preview Modal**: Click to preview document content
- **Download/View Actions**: Action buttons for each document

---

## 🏛️ Grid 4: Past Cases

### **API Endpoint**: `POST /dashboard/populate-hierarchical`
### **Response Field**: `grid_4_cases`

### **UI Components**:
```javascript
{
  "cases": [
    {
      "case_id": "CASE-2023-001",
      "title": "Medical negligence case - Similar pattern",
      "status": "Closed" | "Active" | "Pending",
      "outcome": "Resolved" | "Dismissed" | "Ongoing",
      "similarity_score": 0.85,
      "date": "2023-01-15",
      "jurisdiction": "Maharashtra",
      "key_facts": "Brief summary of key facts"
    }
  ],
  "total_similar": 8,
  "pattern_analysis": "Found 8 similar cases with 75% success rate",
  "success_rate": 0.75
}
```

### **Frontend Implementation**:
- **Case Cards**: Each case as a card with similarity score prominently displayed
- **Similarity Meter**: Visual similarity score (0-100%)
- **Status Badges**: Closed (Green), Active (Blue), Pending (Yellow)
- **Outcome Indicators**: Success/failure indicators with colors
- **Timeline View**: Cases sorted by date with timeline visualization
- **Pattern Analysis Panel**: Summary statistics and success rate
- **Case Details Modal**: Click to view full case details

---

## 🔍 Grid 5: Live Cases Analytics

### **API Endpoint**: `POST /dashboard/populate-hierarchical`
### **Response Field**: `grid_5_live_cases`

### **UI Components**:
```javascript
{
  "message": "✅ LIVE cases analysis completed - Found 15 relevant cases",
  "status": "success" | "demo" | "error",
  "cases": [
    {
      "title": "State vs. Dr. Sharma - Medical Negligence",
      "court": "Delhi High Court",
      "date": "2024-01-15",
      "citation": "2024 DHC 123",
      "summary": "[Medical Negligence | HIGH Priority] Case summary...",
      "similarity_score": 0.92,
      "url": "https://indiankanoon.org/doc/123456/"
    }
  ],
  "total_cases": 15,
  "generation_time": 2.45,
  "api_mode": "live" | "demo"
}
```

### **Frontend Implementation**:
- **Live Status Indicator**: 🟢 LIVE or 🟡 DEMO mode badge
- **Case Cards**: Real-time legal cases with live data indicator
- **Court Hierarchy**: Supreme Court (Gold), High Court (Silver), District (Bronze)
- **Priority Extraction**: Extract and highlight priority from summary
- **Similarity Ranking**: Cases sorted by similarity score
- **External Links**: Direct links to Indian Kanoon case pages
- **Refresh Button**: Manual refresh for latest cases
- **Generation Time**: Show API response time for transparency

---

## 🎮 Interactive Features

### **Dashboard Controls**:
```javascript
// Main dashboard actions
{
  "populate_button": {
    "text": "🎯 Populate Dashboard (Hierarchical)",
    "loading_text": "Analyzing case... (Step X/5)",
    "estimated_time": "45-60 seconds"
  },
  "refresh_grid": {
    "individual_refresh": true, // Each grid can refresh independently
    "auto_refresh": false // Manual refresh only
  },
  "export_options": {
    "pdf_report": true,
    "excel_export": true,
    "json_data": true
  }
}
```

### **Progress Indicators**:
- **Hierarchical Progress**: Show which tier is currently executing
- **Grid Status**: Loading, Success, Error states for each grid
- **Time Estimates**: Show expected completion time
- **Cancellation**: Allow users to cancel long-running operations

---

## 🎨 UI/UX Guidelines

### **Color Scheme**:
- **Primary**: Blue (#2563eb) - Main actions, links
- **Success**: Green (#16a34a) - Completed items, success states
- **Warning**: Yellow (#eab308) - Medium priority, warnings
- **Danger**: Red (#dc2626) - High priority, errors
- **Info**: Gray (#6b7280) - Secondary information

### **Typography**:
- **Headers**: Bold, larger font for grid titles
- **Body**: Regular font for content
- **Monospace**: For case IDs, citations, technical data

### **Responsive Design**:
- **Desktop**: 5-grid layout as shown above
- **Tablet**: 2x3 grid layout (stacked)
- **Mobile**: Single column, collapsible grids

### **Loading States**:
- **Skeleton Loading**: Show placeholder content while loading
- **Progress Bars**: For long-running operations
- **Spinner**: For quick operations

---

## 🔌 API Integration

### **Main Endpoint**:
```javascript
// Primary dashboard population
POST /dashboard/populate-hierarchical
{
  "case_id": "CASE-2024-001",
  "case_context": "Medical malpractice case involving surgical negligence",
  "additional_context": "Patient harm during surgery"
}
```

### **Response Structure**:
```javascript
{
  "grid_1_compliance": { /* Compliance data */ },
  "grid_2_laws": { /* Laws data */ },
  "grid_3_documents": { /* Documents data */ },
  "grid_4_cases": { /* Cases data */ },
  "grid_5_live_cases": { /* Live cases data */ },
  "generation_time": 48.5,
  "ai_confidence": 0.95
}
```

### **Error Handling**:
- **Partial Success**: Show completed grids even if some fail
- **Retry Mechanism**: Allow retry for failed grids
- **Fallback Data**: Show demo data if live data fails

---

## 📱 Mobile Considerations

### **Collapsible Grids**:
- Each grid should be collapsible on mobile
- Show summary statistics in collapsed state
- Expand to show full details

### **Touch Interactions**:
- Swipe gestures for navigation
- Long press for context menus
- Pull-to-refresh for data updates

---

## 🚀 Performance Optimization

### **Lazy Loading**:
- Load grid data progressively
- Virtualize long lists (documents, cases)
- Image lazy loading for document previews

### **Caching**:
- Cache API responses for 5 minutes
- Local storage for user preferences
- Service worker for offline functionality

---

This specification provides everything your frontend engineer needs to implement a comprehensive, user-friendly legal dashboard that matches your backend API structure perfectly! 🎯
