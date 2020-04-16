// pch.cpp: 与预编译标头对应的源文件

#include "pch.h"
#include"stdio.h"

// 当使用预编译的头时，需要使用此源文件，编译才能成功。

typedef struct {
	unsigned char b;
	unsigned char g;
	unsigned char r;
}color_type;

typedef struct {
	unsigned char b;
	unsigned char g;
	unsigned char r;
	unsigned char v;
}list_type;

typedef struct {
	long pix_len;
	long list_len;
}arg_type;



long dis_tens_color(color_type* c1, color_type* c2,unsigned char v)
{
	float temp = 0;
	temp += ((int)c1->b - (int)c2->b) * ((int)c1->b - (int)c2->b);
	temp += ((int)c1->g - (int)c2->g) * ((int)c1->g - (int)c2->g);
	temp += ((int)c1->r - (int)c2->r) * ((int)c1->r - (int)c2->r);
	temp *= (float)v / 50.0;
	return temp;
}

void change_color(color_type* c1, list_type* listPtr, int list_len)
{
	long temp = 0;
	long temp_min = 0;
	color_type* list_temp = (color_type*)(listPtr);
	int i;
	for (i = 0; i < list_len; i++)
	{
		if (i == 0)
		{
			temp = dis_tens_color(c1, (color_type*)(listPtr + i), (listPtr + i)->v);
			temp_min = temp;
			list_temp = (color_type*)(listPtr + i);
		}
		else
		{
			temp = dis_tens_color(c1, (color_type*)(listPtr + i), (listPtr + i)->v);
			if (temp < temp_min)
			{
				list_temp = (color_type*)(listPtr + i);
				temp_min = temp;
			}
		}
	}
	c1->b = list_temp->b;
	c1->g = list_temp->g;
	c1->r = list_temp->r;
}




int img_CV(unsigned char* imgPtr,unsigned char * listPtr,unsigned char * arg_ptr)
{
	arg_type * arg =(arg_type*)arg_ptr;
	long pix_number;
	for (pix_number = 0; pix_number < arg->pix_len; pix_number++)
	{
		change_color((color_type*)(imgPtr)+pix_number,(list_type*)listPtr, arg->list_len);
	}
	return 0;
}


