class Shellgpt < Formula
    desc "ShellGPT: Interact with OpenAI from the shell"
    homepage "https://github.com/adborroto/shellgpt"
    url "https://github.com/adborroto/shellgpt/archive/v1.0.0.tar.gz" 
    sha256 "b602dfee7f18806399762cf54a450ae9f98d217940b99cc23d3fede0897d8387"
    license "MIT"
  
    depends_on "python@3.10" 
  
    def install
      bin.install "shellgpt.py" => "shellgpt"
    end
  
    test do
      system "#{bin}/shellgpt", "--help"
    end
  end
  