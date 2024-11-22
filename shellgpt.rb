class Shellgpt < Formula
    desc "ShellGPT: Interact with OpenAI from the shell"
    homepage "https://github.com/adborroto/shellgpt"
    url "https://github.com/adborroto/shellgpt/archive/v1.0.1.tar.gz" 
    sha256 "4517e46953920c7703d35b1a796ff31480fa81e7a99f4afda86ff138bcdf0576"
    license "MIT"
  
    depends_on "python@3.10" 
  
    def install
      bin.install "shellgpt.py" => "shellgpt"
      system "python3", "-m", "pip", "install", "--upgrade", "pip"
      system "python3", "-m", "pip", "install", "openai"
    end
  
    test do
      system "#{bin}/shellgpt", "--help"
    end
  end
  