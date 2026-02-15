"""Create the sample research papers SQLite database."""

import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "papers.db")

PAPERS = [
    (
        "Attention Is All You Need",
        "Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Lukasz Kaiser, Illia Polosukhin",
        2017,
        "NeurIPS",
        "We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely.",
        95000,
    ),
    (
        "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding",
        "Jacob Devlin, Ming-Wei Chang, Kenton Lee, Kristina Toutanova",
        2019,
        "NAACL",
        "We introduce BERT, a method for pre-training language representations which obtains state-of-the-art results on eleven natural language processing tasks.",
        75000,
    ),
    (
        "Language Models are Few-Shot Learners",
        "Tom B. Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared Kaplan, Prafulla Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell",
        2020,
        "NeurIPS",
        "We demonstrate that scaling up language models greatly improves task-agnostic, few-shot performance, sometimes reaching competitiveness with prior state-of-the-art fine-tuning approaches.",
        32000,
    ),
    (
        "Deep Residual Learning for Image Recognition",
        "Kaiming He, Xiangyu Zhang, Shaoqing Ren, Jian Sun",
        2016,
        "CVPR",
        "We present a residual learning framework to ease the training of networks that are substantially deeper than those used previously.",
        130000,
    ),
    (
        "Playing Atari with Deep Reinforcement Learning",
        "Volodymyr Mnih, Koray Kavukcuoglu, David Silver, Alex Graves, Ioannis Antonoglou, Daan Wierstra, Martin Riedmiller",
        2013,
        "NIPS Workshop",
        "We present the first deep learning model to successfully learn control policies directly from high-dimensional sensory input using reinforcement learning.",
        12000,
    ),
    (
        "Generative Adversarial Nets",
        "Ian J. Goodfellow, Jean Pouget-Abadie, Mehdi Mirza, Bing Xu, David Warde-Farley, Sherjil Ozair, Aaron Courville, Yoshua Bengio",
        2014,
        "NeurIPS",
        "We propose a new framework for estimating generative models via an adversarial process, simultaneously training a generative model and a discriminative model.",
        55000,
    ),
    (
        "Mastering the Game of Go with Deep Neural Networks and Tree Search",
        "David Silver, Aja Huang, Chris J. Maddison, Arthur Guez, Laurent Sifre, George van den Driessche, Julian Schrittwieser, Ioannis Antonoglou, Veda Panneershelvam, Marc Lanctot",
        2016,
        "Nature",
        "We introduce a new approach to computer Go that uses value networks to evaluate board positions and policy networks to select moves, trained by a combination of supervised learning and reinforcement learning.",
        18000,
    ),
    (
        "ImageNet Classification with Deep Convolutional Neural Networks",
        "Alex Krizhevsky, Ilya Sutskever, Geoffrey E. Hinton",
        2012,
        "NeurIPS",
        "We trained a large, deep convolutional neural network to classify the 1.2 million high-resolution images in the ImageNet LSVRC-2010 contest into the 1000 different classes.",
        110000,
    ),
    (
        "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks",
        "Patrick Lewis, Ethan Perez, Aleksandra Piktus, Fabio Petroni, Vladimir Karpukhin, Naman Goyal, Heinrich Kuttler, Mike Lewis, Wen-tau Yih, Tim Rocktaschel, Sebastian Riedel, Douwe Kiela",
        2020,
        "NeurIPS",
        "We explore a general-purpose fine-tuning recipe for retrieval-augmented generation models that combine pre-trained parametric and non-parametric memory for language generation.",
        4500,
    ),
    (
        "Constitutional AI: Harmlessness from AI Feedback",
        "Yuntao Bai, Saurav Kadavath, Sandipan Kundu, Amanda Askell, Jackson Kernion, Andy Jones, Anna Chen, Anna Goldie, Azalia Mirhoseini, Cameron McKinnon",
        2022,
        "arXiv",
        "We propose a method for training a harmless AI assistant through self-improvement, without any human labels identifying harmful outputs.",
        2800,
    ),
    (
        "Scaling Laws for Neural Language Models",
        "Jared Kaplan, Sam McCandlish, Tom Henighan, Tom B. Brown, Benjamin Chess, Rewon Child, Scott Gray, Alec Radford, Jeffrey Wu, Dario Amodei",
        2020,
        "arXiv",
        "We study empirical scaling laws for language model performance on the cross-entropy loss, finding smooth power laws as functions of model size, dataset size, and compute.",
        3200,
    ),
    (
        "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models",
        "Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Brian Ichter, Fei Xia, Ed Chi, Quoc Le, Denny Zhou",
        2022,
        "NeurIPS",
        "We explore how generating a chain of thought -- a series of intermediate reasoning steps -- significantly improves the ability of large language models to perform complex reasoning.",
        5100,
    ),
]


def main():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """
        CREATE TABLE papers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            authors TEXT NOT NULL,
            year INTEGER NOT NULL,
            journal TEXT NOT NULL,
            abstract TEXT NOT NULL,
            citations INTEGER NOT NULL
        )
        """
    )

    conn.executemany(
        "INSERT INTO papers (title, authors, year, journal, abstract, citations) VALUES (?, ?, ?, ?, ?, ?)",
        PAPERS,
    )
    conn.commit()
    conn.close()

    print(f"Created {DB_PATH} with {len(PAPERS)} papers.")


if __name__ == "__main__":
    main()
