class Plot:
    
    def showplot(self, file_name=False):
        import matplotlib  # matplotlib 패키지 불러오기 
        import matplotlib.pyplot as plt # 그래프 시각화를 위한 패키지 불러오기
        import seaborn as sns
        plt.figure(figsize=(20, 6))
        for i in range(110, 1000):
            try : 
                sub = getattr(self, f'subplot{i}')
                if sub[0] == 'count':
                    plt.subplot(sub[1])
                    plt.figure(figsize=(sub[4], sub[5]))
                    sns.countplot(data=sub[2], x=sub[6], palette='viridis')
                    plt.title(sub[3], fontsize=sub[-1], y=1.03)       
                    plt.xlabel(sub[6], fontsize=sub[-1], labelpad=30)                         
                    plt.ylabel('Count', fontsize=sub[-1], rotation=1, labelpad=30)  
                
                elif sub[0] == 'box':
                    plt.subplot(sub[1])
                    sns.boxplot(data=sub[2], x=sub[3], y=sub[4])

            except : 
                continue
        
        if file_name : 
            plt.savefig(f'./{file_name}.png', facecolor='#ffffff') 
        plt.show    
            

    def countplot(self, data, ttl_name, x_name, size_width=15, size_height=7, file_name = False, fontsize=50, inplacesubplot=False) :
        if inplacesubplot: 
            setattr(self, f'subplot{inplacesubplot}', ['count', inplacesubplot, data, ttl_name, size_width, size_height, x_name, fontsize])
            
        else : 
            import seaborn as sns
            import matplotlib.pyplot as plt # 그래프 시각화를 위한 패키지 불러오기
            plt.figure(figsize=(size_width, size_height))

            sns.countplot(data=data, x=x_name, palette='viridis')

            plt.title(ttl_name, fontsize=fontsize, y=1.03)       
            plt.xlabel(x_name, fontsize=fontsize*3/5, labelpad=30)                         
            plt.ylabel('Count', fontsize=fontsize*3/5, rotation=1, labelpad=30)  

            if file_name:
                plt.savefig(f'./plot{file_name}.png', facecolor='#ffffff') 
            plt.show()
            

    def boxplot(self, data, x_name, y_name, inplacesubplot= False) :
        
        if inplacesubplot :
            setattr(self, f'subplot{inplacesubplot}', ['box', inplacesubplot, data, x_name, y_name])
        else : 
            import seaborn as sns
            sns.boxplot(data=data, x=x_name, y=y_name)