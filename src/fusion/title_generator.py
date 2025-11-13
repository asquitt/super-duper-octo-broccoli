"""Generate engaging titles for video clips."""

import re
from typing import List, Dict
import random


class TitleGenerator:
    """Generate click-worthy titles for clips."""

    def __init__(self, config: dict):
        """Initialize title generator with configuration."""
        self.config = config
        self.max_length = config.get('max_length', 60)
        self.style = config.get('style', 'engaging')
        self.include_emoji = config.get('include_emoji', True)

        # Emoji mappings for different contexts
        self.emojis = {
            'surprise': ['🤯', '😱', '🔥', '💥', '✨'],
            'insight': ['💡', '🧠', '💭', '🎯', '⚡'],
            'question': ['🤔', '❓', '🧐', '💬'],
            'excitement': ['🚀', '🎉', '🌟', '⭐', '🔥'],
            'important': ['⚠️', '📢', '🎯', '💎', '🔑'],
            'money': ['💰', '💵', '💸', '🤑'],
            'tech': ['🤖', '💻', '⚙️', '🔧', '📱'],
            'success': ['🏆', '🎯', '✅', '💪', '🎊']
        }

        # Title templates
        self.templates = {
            'engaging': [
                "The {adjective} Secret to {topic}",
                "Why {topic} Changes Everything",
                "The Truth About {topic}",
                "{topic}: What Nobody Tells You",
                "How to {topic} in {time}",
                "The {adjective} Way to {topic}",
                "{number} Things About {topic}",
                "This {topic} Revelation Will Blow Your Mind",
                "The {adjective} Truth Behind {topic}",
                "What {topic} Really Means"
            ],
            'professional': [
                "Understanding {topic}",
                "Key Insights on {topic}",
                "The Fundamentals of {topic}",
                "{topic}: A Deep Dive",
                "Expert Analysis of {topic}",
                "Breaking Down {topic}",
                "{topic} Explained",
                "Critical Points About {topic}"
            ],
            'casual': [
                "Let's Talk About {topic}",
                "{topic} - Here's the Deal",
                "My Take on {topic}",
                "The Real Story of {topic}",
                "{topic} Uncovered",
                "Getting Real About {topic}",
                "What's Up With {topic}"
            ]
        }

        # Power words
        self.adjectives = [
            'Crazy', 'Insane', 'Ultimate', 'Hidden', 'Secret', 'Simple',
            'Shocking', 'Surprising', 'Revolutionary', 'Game-Changing',
            'Mind-Blowing', 'Incredible', 'Amazing', 'Proven', 'Powerful'
        ]

    def generate_title(self, clip: Dict) -> str:
        """
        Generate an engaging title for a clip.

        Args:
            clip: Clip dictionary with scores and text context

        Returns:
            Generated title string
        """
        text_context = clip.get('text_context', '')

        # Extract keywords and topics
        keywords = self._extract_keywords(text_context)

        # Determine clip characteristics
        characteristics = self._analyze_clip_characteristics(clip)

        # Generate title based on style
        if text_context and keywords:
            title = self._generate_from_context(keywords, characteristics)
        else:
            title = self._generate_generic(characteristics)

        # Add emoji if enabled
        if self.include_emoji and self.style == 'engaging':
            title = self._add_emoji(title, characteristics)

        # Ensure length constraint
        title = self._truncate_title(title)

        return title

    def _extract_keywords(self, text: str) -> List[str]:
        """Extract important keywords from text."""
        if not text:
            return []

        # Convert to lowercase
        text = text.lower()

        # Remove punctuation except hyphens
        text = re.sub(r'[^\w\s-]', ' ', text)

        # Split into words
        words = text.split()

        # Stop words to filter
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
            'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
            'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that',
            'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they'
        }

        # Filter keywords (longer than 3 chars, not stop words)
        keywords = [w for w in words if len(w) > 3 and w not in stop_words]

        # Count frequency
        from collections import Counter
        keyword_counts = Counter(keywords)

        # Get top keywords
        top_keywords = [k for k, _ in keyword_counts.most_common(10)]

        return top_keywords

    def _analyze_clip_characteristics(self, clip: Dict) -> Dict:
        """Analyze clip characteristics to guide title generation."""
        characteristics = {
            'high_emotion': clip.get('audio_score', 0) > 0.7,
            'high_topic': clip.get('text_score', 0) > 0.7,
            'high_visual': clip.get('visual_score', 0) > 0.7,
            'overall_score': clip.get('score', 0)
        }

        # Determine dominant modality
        scores = {
            'audio': clip.get('audio_score', 0),
            'text': clip.get('text_score', 0),
            'visual': clip.get('visual_score', 0)
        }
        characteristics['dominant_modality'] = max(scores, key=scores.get)

        return characteristics

    def _generate_from_context(self, keywords: List[str],
                               characteristics: Dict) -> str:
        """Generate title from text context."""
        if not keywords:
            return self._generate_generic(characteristics)

        # Select main topic (first keyword or combination)
        if len(keywords) >= 2:
            topic = f"{keywords[0].title()} {keywords[1].title()}"
        else:
            topic = keywords[0].title()

        # Select template based on style
        templates = self.templates.get(self.style, self.templates['engaging'])
        template = random.choice(templates)

        # Fill template
        title = template.replace('{topic}', topic)

        # Replace other placeholders
        if '{adjective}' in title:
            adjective = random.choice(self.adjectives)
            title = title.replace('{adjective}', adjective)

        if '{time}' in title:
            times = ['Minutes', 'Seconds', 'Steps', 'Days']
            title = title.replace('{time}', random.choice(times))

        if '{number}' in title:
            numbers = ['3', '5', '7', '10']
            title = title.replace('{number}', random.choice(numbers))

        return title

    def _generate_generic(self, characteristics: Dict) -> str:
        """Generate generic title based on characteristics."""
        templates = [
            "Must-See Moment",
            "Key Insight",
            "Important Discussion",
            "Highlight Reel",
            "Critical Point",
            "Game Changer",
            "The Turning Point",
            "Breakthrough Moment"
        ]

        if characteristics['high_emotion']:
            templates.extend([
                "Emotional Revelation",
                "Passionate Discussion",
                "Intense Moment"
            ])

        if characteristics['high_topic']:
            templates.extend([
                "Deep Insight",
                "Key Takeaway",
                "Main Point"
            ])

        if characteristics['high_visual']:
            templates.extend([
                "Visual Highlight",
                "Action Moment",
                "Dynamic Scene"
            ])

        return random.choice(templates)

    def _add_emoji(self, title: str, characteristics: Dict) -> str:
        """Add appropriate emoji to title."""
        # Determine emoji category based on characteristics and title content
        title_lower = title.lower()

        emoji = None

        # Context-based emoji selection
        if any(word in title_lower for word in ['secret', 'hidden', 'truth', 'shocking', 'crazy', 'insane']):
            emoji = random.choice(self.emojis['surprise'])
        elif any(word in title_lower for word in ['insight', 'learn', 'understand', 'key', 'important']):
            emoji = random.choice(self.emojis['insight'])
        elif any(word in title_lower for word in ['question', 'why', 'what', 'how']):
            emoji = random.choice(self.emojis['question'])
        elif any(word in title_lower for word in ['game-chang', 'revolution', 'break']):
            emoji = random.choice(self.emojis['excitement'])
        elif any(word in title_lower for word in ['money', 'cost', 'price', 'cheap', 'expensive']):
            emoji = random.choice(self.emojis['money'])
        elif any(word in title_lower for word in ['ai', 'tech', 'software', 'code', 'algorithm']):
            emoji = random.choice(self.emojis['tech'])
        elif any(word in title_lower for word in ['success', 'win', 'achiev', 'master']):
            emoji = random.choice(self.emojis['success'])
        else:
            # Default based on characteristics
            if characteristics['high_emotion']:
                emoji = random.choice(self.emojis['surprise'])
            elif characteristics['high_topic']:
                emoji = random.choice(self.emojis['insight'])
            else:
                emoji = random.choice(self.emojis['excitement'])

        # Add emoji at the end
        return f"{title} {emoji}"

    def _truncate_title(self, title: str) -> str:
        """Truncate title to max length."""
        if len(title) <= self.max_length:
            return title

        # Try to truncate at word boundary
        truncated = title[:self.max_length]

        # Find last space
        last_space = truncated.rfind(' ')

        if last_space > self.max_length * 0.8:  # At least 80% of desired length
            truncated = truncated[:last_space]

        # Add ellipsis if we cut off text (but not emoji)
        if not truncated.endswith(('!', '?', '.')):
            # Check if there's an emoji at the end
            if truncated and ord(truncated[-1]) > 127:  # Unicode emoji
                return truncated
            else:
                return truncated + "..."

        return truncated
