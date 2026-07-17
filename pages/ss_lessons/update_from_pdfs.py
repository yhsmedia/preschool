#!/usr/bin/env python3
import re
from pathlib import Path

pdf_lessons = {
    "creation-part-1.md": {"week": "1", "page": "18", "quarter": "Following after God - Spring", "season": "Spring 2026", "quarter-number": "4", "year": "2026", "description": "God made all things.", "memory-verse": "\"In the beginning God created the heaven and the earth.\" Genesis 1:1"},
    "creation-part-2.md": {"week": "2", "page": "20", "quarter": "Following after God - Spring", "season": "Spring 2026", "quarter-number": "4", "year": "2026", "description": "God made us different from the animals; we are very special to Him.", "memory-verse": "\"In the beginning God created the heaven and the earth.\" Genesis 1:1"},
    "adam-and-eve.md": {"week": "3", "page": "22", "quarter": "Following after God - Spring", "season": "Spring 2026", "quarter-number": "4", "year": "2026", "description": "God wants us to obey Him.", "memory-verse": "Review previous verse"},
    "heaven.md": {"week": "4", "page": "24", "quarter": "Following after God - Spring", "season": "Spring 2026", "quarter-number": "4", "year": "2026", "description": "Jesus is the only way to heaven; we must ask Him to forgive our sins.", "memory-verse": "\"I am the way, the truth, and the life: no man cometh unto the Father, but by me.\" John 14:6"},
    "triumphal-entry-and-last-supper.md": {"week": "A", "page": "12", "quarter": "Following after God - Spring", "season": "Spring 2026", "quarter-number": "4", "year": "2026", "description": "God loves us and sent Jesus to die for our sins.", "memory-verse": "\"For God so loved the world, that he gave his only begotten Son, that whosoever believeth in him should not perish, but have everlasting life.\" John 3:16"},
    "christs-crucifixion-and-resurrection.md": {"week": "B", "page": "14", "quarter": "Following after God - Spring", "season": "Spring 2026", "quarter-number": "4", "year": "2026", "description": "Jesus took the punishment for our sins.", "memory-verse": "Review previous verse"},
    "jesus-appears-alive-and-returns-to-heaven.md": {"week": "C", "page": "16", "quarter": "Following after God - Spring", "season": "Spring 2026", "quarter-number": "4", "year": "2026", "description": "Jesus will come again someday and take His children to heaven.", "memory-verse": "Review previous verse"},
    "naaman-and-the-servant-girl-part-1.md": {"week": "5", "page": "26", "quarter": "Following after God - Spring", "season": "Spring 2026", "quarter-number": "4", "year": "2026", "description": "We should be kind to others, even if it is hard.", "memory-verse": "\"I am the way, the truth, and the life: no man cometh unto the Father, but by me.\" John 14:6"},
    "naaman-and-the-servant-girl-part-2.md": {"week": "6", "page": "28", "quarter": "Following after God - Spring", "season": "Spring 2026", "quarter-number": "4", "year": "2026", "description": "We should obey God, even when we don't want to.", "memory-verse": "Review previous verses"},
    "lost-lamb.md": {"week": "7", "page": "30", "quarter": "Following after God - Spring", "season": "Spring 2026", "quarter-number": "4", "year": "2026", "description": "God loves us even when we sin.", "memory-verse": "Review previous verses"},
    "joseph.md": {"week": "8", "page": "32", "quarter": "Following after God - Spring", "season": "Spring 2026", "quarter-number": "4", "year": "2026", "description": "We should be kind and forgiving even when we are mistreated.", "memory-verse": "\"I will be sorry for my sin.\" Psalm 38:18"},
    "jonah-part-1.md": {"week": "9", "page": "34", "quarter": "Following after God - Spring", "season": "Spring 2026", "quarter-number": "4", "year": "2026", "description": "It is important to obey the first time we are told to do something.", "memory-verse": "Review all four verses"},
    "jonah-part-2.md": {"week": "10", "page": "36", "quarter": "Following after God - Spring", "season": "Spring 2026", "quarter-number": "4", "year": "2026", "description": "Obeying God is better than having our own way.", "memory-verse": "Review all four verses"},

    "follow-me.md": {"week": "1", "page": "20", "quarter": "Gods Word and Me - Winter", "season": "Winter 2025-2026", "quarter-number": "3", "year": "2025-2026", "description": "We can bring people to Jesus.", "memory-verse": "\"Even a child is known by his doings.\" Proverbs 20:11"},
    "noah-obeys-god-part-1.md": {"week": "2", "page": "22", "quarter": "Gods Word and Me - Winter", "season": "Winter 2025-2026", "quarter-number": "3", "year": "2025-2026", "description": "We can do right even when it is hard.", "memory-verse": "Review previous verse"},
    "jesus-is-born-part-1.md": {"week": "A", "page": "12", "quarter": "Gods Word and Me - Winter", "season": "Winter 2025-2026", "quarter-number": "3", "year": "2025-2026", "description": "God keeps His promises.", "memory-verse": "\"Christ Jesus came into the world to save sinners.\" 1 Timothy 1:15"},
    "jesus-is-born-part-2.md": {"week": "B", "page": "14", "quarter": "Gods Word and Me - Winter", "season": "Winter 2025-2026", "quarter-number": "3", "year": "2025-2026", "description": "God chooses special helpers; you can be one, too.", "memory-verse": "Review previous verse"},
    "kings-worship-jesus.md": {"week": "C", "page": "16", "quarter": "Gods Word and Me - Winter", "season": "Winter 2025-2026", "quarter-number": "3", "year": "2025-2026", "description": "The best gift we can give Jesus is our heart.", "memory-verse": "Review previous verse"},
    "jesus-boyhood.md": {"week": "D", "page": "18", "quarter": "Gods Word and Me - Winter", "season": "Winter 2025-2026", "quarter-number": "3", "year": "2025-2026", "description": "God will help us to obey.", "memory-verse": "\"Even a child is known by his doings.\" Proverbs 20:11"},
    "noah-obeys-god-part-2.md": {"week": "3", "page": "24", "quarter": "Gods Word and Me - Winter", "season": "Winter 2025-2026", "quarter-number": "3", "year": "2025-2026", "description": "God takes care of us.", "memory-verse": "\"Call unto me, and I will answer thee, and shew thee great and mighty things.\" Jeremiah 33:3"},
    "abraham-and-lot.md": {"week": "4", "page": "26", "quarter": "Gods Word and Me - Winter", "season": "Winter 2025-2026", "quarter-number": "3", "year": "2025-2026", "description": "Be kind and share.", "memory-verse": "Review previous verse"},
    "isaac-the-promised-son.md": {"week": "5", "page": "28", "quarter": "Gods Word and Me - Winter", "season": "Winter 2025-2026", "quarter-number": "3", "year": "2025-2026", "description": "Wait on the Lord; He will answer your prayers.", "memory-verse": "Review previous verse"},
    "bride-for-isaac.md": {"week": "6", "page": "30", "quarter": "Gods Word and Me - Winter", "season": "Winter 2025-2026", "quarter-number": "3", "year": "2025-2026", "description": "Always finish the job you are given to do.", "memory-verse": "Review previous verse"},
    "baby-moses.md": {"week": "7", "page": "32", "quarter": "Gods Word and Me - Winter", "season": "Winter 2025-2026", "quarter-number": "3", "year": "2025-2026", "description": "Always keep your promises.", "memory-verse": "\"As for God, his way is perfect.\" Psalm 18:30"},
    "hannah-prays-for-a-son.md": {"week": "8", "page": "34", "quarter": "Gods Word and Me - Winter", "season": "Winter 2025-2026", "quarter-number": "3", "year": "2025-2026", "description": "We should obey those who have authority over us.", "memory-verse": "Review previous verse"},
    "samuel-listens-to-god.md": {"week": "9", "page": "36", "quarter": "Gods Word and Me - Winter", "season": "Winter 2025-2026", "quarter-number": "3", "year": "2025-2026", "description": "God cares for us.", "memory-verse": "Review previous verse"},

    "jesus-loves-the-children.md": {"week": "1", "page": "12", "quarter": "Going Gods Way - Fall", "season": "Fall 2025", "quarter-number": "6", "year": "2025", "description": "Jesus loves us and is our friend.", "memory-verse": "\"We love him, because he first loved us.\" 1 John 4:19"},
    "noblemans-son.md": {"week": "2", "page": "14", "quarter": "Going Gods Way - Fall", "season": "Fall 2025", "quarter-number": "6", "year": "2025", "description": "Jesus knows all things.", "memory-verse": "Review previous verse"},
    "jesus-raises-jairuss-daughter.md": {"week": "3", "page": "16", "quarter": "Going Gods Way - Fall", "season": "Fall 2025", "quarter-number": "6", "year": "2025", "description": "Jesus cares about us when we are sick.", "memory-verse": "Review previous verse"},
    "friends-at-bethany.md": {"week": "4", "page": "18", "quarter": "Going Gods Way - Fall", "season": "Fall 2025", "quarter-number": "6", "year": "2025", "description": "We should tell Jesus we love Him every day.", "memory-verse": "\"Love one another.\" 1 John 3:23"},
    "blind-bartimaeus.md": {"week": "5", "page": "20", "quarter": "Going Gods Way - Fall", "season": "Fall 2025", "quarter-number": "6", "year": "2025", "description": "We should love Jesus and tell our friends about Him, too.", "memory-verse": "Review previous verses"},
    "jesus-heals-the-paralyzed-man.md": {"week": "6", "page": "22", "quarter": "Going Gods Way - Fall", "season": "Fall 2025", "quarter-number": "6", "year": "2025", "description": "We should always be willing to help a friend.", "memory-verse": "Review previous verses"},
    "fishing-with-jesus.md": {"week": "7", "page": "24", "quarter": "Going Gods Way - Fall", "season": "Fall 2025", "quarter-number": "6", "year": "2025", "description": "Jesus knows all things.", "memory-verse": "\"Be ye kind one to another, tenderhearted, forgiving one another.\" Ephesians 4:32"},
    "jesus-stills-the-storm.md": {"week": "8", "page": "26", "quarter": "Going Gods Way - Fall", "season": "Fall 2025", "quarter-number": "6", "year": "2025", "description": "The wind and the waves obey Jesus, and we should obey Him, too.", "memory-verse": "Review previous verses"},
    "peter-is-free.md": {"week": "9", "page": "28", "quarter": "Going Gods Way - Fall", "season": "Fall 2025", "quarter-number": "6", "year": "2025", "description": "We should pray for our friends.", "memory-verse": "Review previous verses"},
    "elisha-helps-a-widow-lady.md": {"week": "10", "page": "30", "quarter": "Going Gods Way - Fall", "season": "Fall 2025", "quarter-number": "6", "year": "2025", "description": "We should show our friends that we care about them.", "memory-verse": "Review previous verses"},
    "elisha-raises-the-shunammites-son.md": {"week": "11", "page": "32", "quarter": "Going Gods Way - Fall", "season": "Fall 2025", "quarter-number": "6", "year": "2025", "description": "God hears and answers prayer.", "memory-verse": "\"O give thanks unto the Lord; for he is good.\" Psalm 106:1"},
    "king-david-is-kind.md": {"week": "13", "page": "36", "quarter": "Going Gods Way - Fall", "season": "Fall 2025", "quarter-number": "6", "year": "2025", "description": "We should be kind to our friends.", "memory-verse": "Review all four verses"},
    "first-thanksgiving.md": {"week": "12", "page": "34", "quarter": "Going Gods Way - Fall", "season": "Fall 2025", "quarter-number": "6", "year": "2025", "description": "Always remember to thank God for the wonderful country we live in.", "memory-verse": "Review all four verses"},

    "rise-up-and-walk.md": {"week": "1", "page": "12", "quarter": "Growing Up with Jesus - Summer", "season": "Summer 2025", "quarter-number": "5", "year": "2025", "description": "There is power in Jesus' name.", "memory-verse": "\"All things were made by him.\" John 1:3"},
    "safe-outside-the-wall.md": {"week": "2", "page": "14", "quarter": "Growing Up with Jesus - Summer", "season": "Summer 2025", "quarter-number": "5", "year": "2025", "description": "The power of Jesus changes lives.", "memory-verse": "Review previous verse"},
    "saul-and-barnabas-team-up.md": {"week": "3", "page": "16", "quarter": "Growing Up with Jesus - Summer", "season": "Summer 2025", "quarter-number": "5", "year": "2025", "description": "Share the news of Jesus Christ.", "memory-verse": "\"Blessed are they that hear the word of God, and keep it.\" Luke 11:28"},
    "philippian-jailer.md": {"week": "4", "page": "18", "quarter": "Growing Up with Jesus - Summer", "season": "Summer 2025", "quarter-number": "5", "year": "2025", "description": "Jesus saves.", "memory-verse": "Review previous verse"},
    "timothy-learns-god-s-word.md": {"week": "5", "page": "20", "quarter": "Growing Up with Jesus - Summer", "season": "Summer 2025", "quarter-number": "5", "year": "2025", "description": "God wants us to learn His Word.", "memory-verse": "Review previous verses"},
    "a-brave-young-boy.md": {"week": "6", "page": "22", "quarter": "Growing Up with Jesus - Summer", "season": "Summer 2025", "quarter-number": "5", "year": "2025", "description": "God helps us when we are afraid.", "memory-verse": "Review previous verses"},
    "which-man-was-forgiven.md": {"week": "7", "page": "24", "quarter": "Growing Up with Jesus - Summer", "season": "Summer 2025", "quarter-number": "5", "year": "2025", "description": "All have sinned and need a Savior.", "memory-verse": "Review previous verses"},
    "little-and-lost.md": {"week": "8", "page": "26", "quarter": "Growing Up with Jesus - Summer", "season": "Summer 2025", "quarter-number": "5", "year": "2025", "description": "Each one is important to God.", "memory-verse": "\"Even the winds and the sea obey him!\" Matthew 8:27"},
    "wise-and-foolish-builders.md": {"week": "9", "page": "28", "quarter": "Growing Up with Jesus - Summer", "season": "Summer 2025", "quarter-number": "5", "year": "2025", "description": "Build your life on God's Word.", "memory-verse": "Review previous verses"},
    "unforgiving-servant.md": {"week": "10", "page": "30", "quarter": "Growing Up with Jesus - Summer", "season": "Summer 2025", "quarter-number": "5", "year": "2025", "description": "Since God forgives, we ought to forgive.", "memory-verse": "\"Children, obey your parents in all things: for this is well pleasing unto the Lord.\" Colossians 3:20"},
    "which-son-obeyed.md": {"week": "11", "page": "32", "quarter": "Growing Up with Jesus - Summer", "season": "Summer 2025", "quarter-number": "5", "year": "2025", "description": "Trust Jesus and obey.", "memory-verse": "Review all four verses"},
    "midnight-visitor.md": {"week": "12", "page": "34", "quarter": "Growing Up with Jesus - Summer", "season": "Summer 2025", "quarter-number": "5", "year": "2025", "description": "Keep praying.", "memory-verse": "Review all four verses"},
    "who-is-my-neighbor.md": {"week": "13", "page": "36", "quarter": "Growing Up with Jesus - Summer", "season": "Summer 2025", "quarter-number": "5", "year": "2025", "description": "God wants us to be kind to everyone.", "memory-verse": "Review all four verses"},

    "ruth-makes-the-right-choice.md": {"week": "1", "page": "22", "quarter": "Growing in Gods Word - Spring", "season": "Spring 2025", "quarter-number": "4", "year": "2025", "description": "Trusting in God", "memory-verse": "\"Every good gift and every perfect gift is from above.\" James 1:17"},
    "god-cares-for-ruth.md": {"week": "2", "page": "24", "quarter": "Growing in Gods Word - Spring", "season": "Spring 2025", "quarter-number": "4", "year": "2025", "description": "Serving God", "memory-verse": "Review previous verse"},
    "twins-are-different.md": {"week": "3", "page": "26", "quarter": "Growing in Gods Word - Spring", "season": "Spring 2025", "quarter-number": "4", "year": "2025", "description": "Honoring God", "memory-verse": "\"The Lord is good to all.\" Psalm 145:9"},
    "a-rock-for-a-pillow.md": {"week": "4", "page": "28", "quarter": "Growing in Gods Word - Spring", "season": "Spring 2025", "quarter-number": "4", "year": "2025", "description": "God keeps His promises", "memory-verse": "Review previous verse"},
    "brothers-forgive.md": {"week": "5", "page": "30", "quarter": "Growing in Gods Word - Spring", "season": "Spring 2025", "quarter-number": "4", "year": "2025", "description": "God forgives", "memory-verse": "Review previous verse"},
    "people-worship-jesus.md": {"week": "A", "page": "12", "quarter": "Growing in Gods Word - Spring", "season": "Spring 2025", "quarter-number": "4", "year": "2025", "description": "Jesus is God and is worthy of all worship and praise", "memory-verse": "\"For all have sinned, and come short of the glory of God.\" Romans 3:23"},
    "jesus-dies-and-lives-again.md": {"week": "B", "page": "14", "quarter": "Growing in Gods Word - Spring", "season": "Spring 2025", "quarter-number": "4", "year": "2025", "description": "Jesus paid the punishment for our sin", "memory-verse": "Review previous verse"},
    "jesus-appears-to-his-friends.md": {"week": "C", "page": "16", "quarter": "Growing in Gods Word - Spring", "season": "Spring 2025", "quarter-number": "4", "year": "2025", "description": "Jesus Christ arose and was seen by many", "memory-verse": "Review previous verse"},
    "eating-breakfast-with-jesus.md": {"week": "D", "page": "18", "quarter": "Growing in Gods Word - Spring", "season": "Spring 2025", "quarter-number": "4", "year": "2025", "description": "Jesus wants to be our friend", "memory-verse": "\"Every good gift and every perfect gift is from above.\" James 1:17"},
    "jesus-returns-to-heaven.md": {"week": "E", "page": "20", "quarter": "Growing in Gods Word - Spring", "season": "Spring 2025", "quarter-number": "4", "year": "2025", "description": "Jesus is alive, preparing a place in Heaven, and will return for His own", "memory-verse": "Review previous verses"},
    "marching-round-and-round.md": {"week": "6", "page": "32", "quarter": "Growing in Gods Word - Spring", "season": "Spring 2025", "quarter-number": "4", "year": "2025", "description": "God helps", "memory-verse": "\"Fear not, for I am with thee.\" Genesis 26:24"},
    "joshua-keeps-his-promise.md": {"week": "7", "page": "34", "quarter": "Growing in Gods Word - Spring", "season": "Spring 2025", "quarter-number": "4", "year": "2025", "description": "Ask God first / Promises should be kept", "memory-verse": "Review all four verses"},
    "a-few-good-men.md": {"week": "8", "page": "36", "quarter": "Growing in Gods Word - Spring", "season": "Spring 2025", "quarter-number": "4", "year": "2025", "description": "God's power", "memory-verse": "Review all four verses"},
}


def update_yaml_front_matter(file_path, updates):
    content = file_path.read_text()
    if not content.startswith('---'):
        return False

    parts = content.split('---', 2)
    if len(parts) < 3:
        return False

    front_matter = parts[1]
    body = parts[2]

    for key, value in updates.items():
        pattern = f'^{key}: .*?$'
        replacement = f'{key}: "{value}"'
        front_matter = re.sub(pattern, replacement,
                              front_matter, flags=re.MULTILINE)

    new_content = f'---{front_matter}---{body}'
    file_path.write_text(new_content)
    return True


root = Path('.')
updated = 0
for filename, data in pdf_lessons.items():
    file_path = root / filename
    if file_path.exists():
        if update_yaml_front_matter(file_path, data):
            updated += 1
            print(f"Updated: {filename}")
        else:
            print(f"Failed: {filename}")
    else:
        print(f"Not found: {filename}")

print(f"\nTotal updated: {updated}")
