# -*- coding: utf-8 -*-


from __future__ import division


import re



class SummaryTool(object):

    # method for splitting a text into sentences
    def split_content_to_sentences(self, content):
        content = content.replace("\n", ". ")
        return content.split(". ")

    # method for splitting a text into paragraphs
    def split_content_to_paragraphs(self, content):
        return content.split("\n\n")

    # Caculate the intersection between 2 sentences
    def sentences_intersection(self, sent1, sent2):

        # split the sentence into words/tokens
        s1 = set(sent1.split(" "))
        s2 = set(sent2.split(" "))

        # If there is not intersection, just return 0
        if (len(s1) + len(s2)) == 0:
            return 0

        # We normalize the result by the average number of words
        return len(s1.intersection(s2)) / ((len(s1) + len(s2)) / 2)

    # Format a sentence - remove all non-alphbetic chars from the sentence
    # We'll use the formatted sentence as a key in our sentences dictionary
    def format_sentence(self, sentence):
        sentence = re.sub(r'\W+', '', sentence)
        return sentence

    # Convert the content into a dictionary <K, V>
    # k = The formatted sentence
    # V = The rank of the sentence
    def get_senteces_ranks(self, content):

        # Split the content into sentences
        sentences = self.split_content_to_sentences(content)

        # Calculate the intersection of every two sentences
        n = len(sentences)
        values = [[0 for x in xrange(n)] for x in xrange(n)]
        for i in range(0, n):
            for j in range(0, n):
                values[i][j] = self.sentences_intersection(sentences[i], sentences[j])

        # Build the sentences dictionary
        # The score of a sentences is the sum of all its intersection
        sentences_dic = {}
        for i in range(0, n):
            score = 0
            for j in range(0, n):
                if i == j:
                    continue
                score += values[i][j]
            sentences_dic[self.format_sentence(sentences[i])] = score
        return sentences_dic

    # Return the best sentence in a paragraph
    def get_best_sentence(self, paragraph, sentences_dic):

        # Split the paragraph into sentences
        sentences = self.split_content_to_sentences(paragraph)

        # Ignore short paragraphs
        if len(sentences) < 2:
            return ""

        # Get the best sentence according to the sentences dictionary
        best_sentence = ""
        max_value = 0
        for s in sentences:
            strip_s = self.format_sentence(s)
            if strip_s:
                if sentences_dic[strip_s] > max_value:
                    max_value = sentences_dic[strip_s]
                    best_sentence = s

        return best_sentence

    # Build the summary
    def get_summary(self, title, content, sentences_dic):

        # Split the content into paragraphs
        paragraphs = self.split_content_to_paragraphs(content)

        # Add the title
        summary = []
        summary.append(title.strip())
        summary.append("")

        # Add the best sentence from each paragraph
        for p in paragraphs:
            sentence = self.get_best_sentence(p, sentences_dic).strip()
            if sentence:
                summary.append(sentence)

        return ("\n").join(summary)


# Main method, just run "python summary_tool.py"
def main():

   
    title = """
    DANGAL
    """

    content ="""Mahavir Singh Phogat is an amateur wrestler who was forced to give up wrestling in order to obtain gainful employment. He was unable to win a gold medal for India and vows that his son will. He is disappointed when his wife gives birth to four daughters. He gives up his dream thinking that girls cannot wrestle and should only be taught household chores. But when his older daughters, Geeta and Babita, come home after beating up two boys in response to derogatory comments, Mahavir realises his daughters have the potential to become wrestlers.

Mahavir begins coaching Geeta and Babita in wrestling. His methods seem harsh, including grueling early morning workouts and short haircuts to avoid lice. Initially, the girls resent their father for his treatment but they soon realise that their father wants them to have a future and not grow up to be stereotypical housewives. The girls become motivated and willingly participate in Mahavir's coaching. Mahavir takes the girls to wrestling tournaments. Geeta and Babita both wrestle with boys and beat them, much to everyone's dismay. Geeta eventually wins the Junior Nationals and goes to an institute in Patiala for further training so that she can participate in the Commonwealth Games.

Geeta makes friends at the institute and begins to disregard the discipline she has been brought up with. She regularly watches TV, eats street food, and grows her hair longer. Her coach's training differs significantly from her father's techniques. Geeta believes her coach's techniques are better and that Mahavir's techniques are outdated. On a visit home, she is determined to show her father she can wrestle well without his techniques. This leads to a ferocious bout between Geeta and Mahavir. Mahavir loses against Geeta due to his age. Babita tells Geeta that she shouldn't forget her father's techniques and reminds her that it is because of their father that she is where she is now.

Babita soon follows Geeta to the institute. Geeta finds herself losing every match as she is not following her father's techniques or she is not fully focused on wrestling (painting her nails and growing her hair long). Realising her error, she tearfully makes peace with Mahavir. Mahavir comes to Patiala and begins coaching Geeta and Babita secretly, using the same methods as when they were younger. Their coach comes to know about this and is furious with Mahavir's interference and wants to expel them both from the institution, but a deal is struck to allow them to continue as long as Mahavir does not enter the institution or train them elsewhere. Determined to continue assisting his daughters, Mahavir obtains tapes of Geeta's previous unsuccessful bouts and coaches her by pointing out her errors over the phone.

During Geeta's bouts in the Commonwealth Games, Mahavir constantly contradicts her coach's instructions while sitting in the audience. Geeta disregards her coach and follows her father's instructions and wins every bout. Just before the final bout, Geeta's jealous coach conspires to lock Mahavir in a closet far away from the arena. Due to her father's absence, Geeta starts lagging behind in the bout where she manages to win the first round but loses the second. It's the final round and the score is 4-1 where Geeta is down.In the last handful of seconds Geeta becomes desperate to win some points but in return loses another. Now, the score is 5-1. Only a quarter of the final minute is left, and now, Geeta starts recalling her father's teachings. She recalls her father talking about a 5 pointer suplex back when she was young. Mahavir said that the suplex is difficult but can be applied. She also recalls her father saying that one has to play with the opponent's mind. Mahavir said that one has to show something and do something else. Combining these two teachings, Geeta gives her opponent a suplex in the final 3 seconds, leading to a score of 6-5 (Geeta being up) and becomes the first Indian female wrestler to win gold. Mahavir returns just in time to embrace his daughters, frustrating the coach's hopes of obtaining credit before the news media.

The end credits reveal that Babita also won a silver medal in wrestling at the Commonwealth Games in 2014, Geeta became the first Indian female wrestler to qualify for the Olympics and Mahavir's efforts inspired dozens of Indian women to participate in wrestling."""

    
    

    # Create a SummaryTool object
    st = SummaryTool()

    # Build the sentences dictionary
    sentences_dic = st.get_senteces_ranks(content)

    # Build the summary with the sentences dictionary
    summary = st.get_summary(title, content, sentences_dic)

    # Print the summary
    print summary

    # Print the ratio between the summary length and the original length
    print ""
    print "Original Length %s" % (len(title) + len(content))
    print "Summary Length %s" % len(summary)
    print "Summary Ratio: %s" % (100 - (100 * (len(summary) / (len(title) + len(content)))))


if __name__ == '__main__':
 main()
 

