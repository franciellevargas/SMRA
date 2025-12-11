
# this is from the diagram that Fran sent
definition="""Hate Speech can result due to some of the followngs:
- Having a term or expression with any pejorative connotation.
- Having a sequence of swear words.
- Having a sequence of at least two terms, or/and expressions with any pejorative connotation expressed explicitly or implicitly.
"""
base_prompt_for_hate = """Analyze the following text "{text}" for hate speech.
Provide your analysis in this exact format:
hate_label: [YES if the text contains hate speech, NO otherwise]
Provide ONLY the required output format with no additional text, explanations, or justifications.
"""
base_prompt_for_moral = """Identify the underlying moral value dimensions in the following text "{text}".
The Moral Foundations Theory framework represents core ethical ad psychological concerns that come in paired positive vs negative expressions:
- care vs harm: Involves concern for the well-being of others, with virtues expressed through care, protection, or nurturance, and vices involving harm, cruelty, or indifference to suffering.
- fairness vs cheating: morals related to justice, rights, and reciprocity, with fairness indicating equity, rule-following, and cheating denoting exploitation, dishonesty, or manipulation.
- loyalty vs betrayal: morals related to group-based morality, where loyalty refers to solidarity, allegiance, and in-group defense, while betrayal signals disloyalty or abandonment of one’s group.
- authority vs subversion: morals related to respect for tradition, and legitimate hierarchies, with authority indicating respect or deference to leadership or norms, and subversion indicating rebellion, disrespect, or disobedience.
- sanctity vs degradation: morals related to purity, contamination, with Purity is associated with cleanliness, modesty, or moral elevation, while degradation includes defilement, obscenity,or perceived corruption.

Provide your analysis in this exact format:
moral_value: [the single most prominent moral foundations from: care, harm, fairness, cheating, authority, subversion, sanctity, degradation, loyalty, betrayal. If no clear moral foundation applies, write "None"]
explanation: [provide a brief evidence based justification, specifically highlighting the words or phrases that triggered your moral value classification. If none, write "None"]

Provide ONLY the required output format with no additional text, explanations, or justifications.
"""

# this is the same prompt from the previous work
hate_moral_combined = """Analyze the following text "{text}" for hate speech and identify its underlying moral value dimensions:
The Moral Foundations Theory framework represents core ethical ad psychological concerns that come in paired positive vs negative expressions:
- care vs harm: Involves concern for the well-being of others, with virtues expressed through care, protection, or nurturance, and vices involving harm, cruelty, or indifference to suffering.
- fairness vs cheating: morals related to justice, rights, and reciprocity, with fairness indicating equity, rule-following, and cheating denoting exploitation, dishonesty, or manipulation.
- loyalty vs betrayal: morals related to group-based morality, where loyalty refers to solidarity, allegiance, and in-group defense, while betrayal signals disloyalty or abandonment of one’s group.
- authority vs subversion: morals related to respect for tradition, and legitimate hierarchies, with authority indicating respect or deference to leadership or norms, and subversion indicating rebellion, disrespect, or disobedience.
- sanctity vs degradation: morals related to purity, contamination, with Purity is associated with cleanliness, modesty, or moral elevation, while degradation includes defilement, obscenity,or perceived corruption.

Provide your analysis in this exact format:
hate_label: [YES if the text contains hate speech, NO otherwise]
moral_value: [the single most prominent moral foundations from: care, harm, fairness, cheating, authority, subversion, sanctity, degradation, loyalty, betrayal. If no clear moral foundation applies, write "None"]
explanation: [provide a brief evidence based justification, specifically highlighting the words or phrases that triggered your moral value classification. If none, write "None"]

Provide ONLY the required output format with no additional text, explanations, or justifications."""

hate_with_definition = """Analyze the following text "{text}" for hate speech.
{definition}

Provide your analysis in this exact format:
hate_label: [YES if the text contains hate speech, NO otherwise]
Provide ONLY the required output format with no additional text, explanations, or justifications.
"""

moral_with_definition = """Identify the underlying moral value dimensions in the following text "{text}".
The Moral Foundations Theory framework represents core ethical ad psychological concerns that come in paired positive vs negative expressions:
- care vs harm: Involves concern for the well-being of others, with virtues expressed through care, protection, or nurturance, and vices involving harm, cruelty, or indifference to suffering.
- fairness vs cheating: morals related to justice, rights, and reciprocity, with fairness indicating equity, rule-following, and cheating denoting exploitation, dishonesty, or manipulation.
- loyalty vs betrayal: morals related to group-based morality, where loyalty refers to solidarity, allegiance, and in-group defense, while betrayal signals disloyalty or abandonment of one’s group.
- authority vs subversion: morals related to respect for tradition, and legitimate hierarchies, with authority indicating respect or deference to leadership or norms, and subversion indicating rebellion, disrespect, or disobedience.
- sanctity vs degradation: morals related to purity, contamination, with Purity is associated with cleanliness, modesty, or moral elevation, while degradation includes defilement, obscenity,or perceived corruption.
{definition}

Provide your analysis in this exact format:
moral_value: [the single most prominent moral foundations from: care, harm, fairness, cheating, authority, subversion, sanctity, degradation, loyalty, betrayal. If no clear moral foundation applies, write "None"]
explanation: [provide a brief evidence based justification, specifically highlighting the words or phrases that triggered your moral value classification. If none, write "None"]

Provide ONLY the required output format with no additional text, explanations, or justifications.
"""

hate_moral_combined_with_definition = """Analyze the following text "{text}" for hate speech and identify its underlying moral value dimensions:
The Moral Foundations Theory framework represents core ethical ad psychological concerns that come in paired positive vs negative expressions:
- care vs harm: Involves concern for the well-being of others, with virtues expressed through care, protection, or nurturance, and vices involving harm, cruelty, or indifference to suffering.
- fairness vs cheating: morals related to justice, rights, and reciprocity, with fairness indicating equity, rule-following, and cheating denoting exploitation, dishonesty, or manipulation.
- loyalty vs betrayal: morals related to group-based morality, where loyalty refers to solidarity, allegiance, and in-group defense, while betrayal signals disloyalty or abandonment of one’s group.
- authority vs subversion: morals related to respect for tradition, and legitimate hierarchies, with authority indicating respect or deference to leadership or norms, and subversion indicating rebellion, disrespect, or disobedience.
- sanctity vs degradation: morals related to purity, contamination, with Purity is associated with cleanliness, modesty, or moral elevation, while degradation includes defilement, obscenity,or perceived corruption.
{definition}

Provide your analysis in this exact format:
hate_label: [YES if the text contains hate speech, NO otherwise]
moral_value: [the single most prominent moral foundations from: care, harm, fairness, cheating, authority, subversion, sanctity, degradation, loyalty, betrayal. If no clear moral foundation applies, write "None"]
explanation: [provide a brief evidence based justification, specifically highlighting the words or phrases that triggered your moral value classification. If none, write "None"]

Provide ONLY the required output format with no additional text, explanations, or justifications."""


