class Shellgpt < Formula
    desc "ShellGPT: Interact with OpenAI from the shell"
    homepage "https://github.com/adborroto/homebrew-shellgpt"
    url "https://github.com/adborroto/homebrew-shellgptpython/archive/v1.0.1.tar.gz" 
    sha256 "4517e46953920c7703d35b1a796ff31480fa81e7a99f4afda86ff138bcdf0576"
    license "MIT"
  
    depends_on "python@3.10" 
  
    def install
        ENV.prepend_create_path "PYTHONPATH", libexec/"lib/python3.10/site-packages"
        system "python3", "-m", "venv", libexec
    
        system libexec/"bin/pip", "install", "--upgrade", "pip", "setuptools", "wheel"
        system libexec/"bin/pip", "install", "openai"
    
        bin.install "shellgpt.py" => "shellgpt"
    
        (bin/"shellgpt").write_env_script libexec/"bin/python3", libexec/"bin/shellgpt.py"
      end
  
    test do
      system "#{bin}/shellgpt", "--help"
    end
  end
  