// pch.cpp: 与预编译标头对应的源文件

#include "pch.h"
// 当使用预编译的头时，需要使用此源文件，编译才能成功。
#include"stdio.h"
typedef struct {
	unsigned char b;
	unsigned char g;
	unsigned char r;
}color_type;


typedef struct {
	long pix_len;
	long list_len;
}arg_type;



long dis_tens_color(color_type* c1, color_type* c2)
{
	float temp = 0;
	temp += ((int)c1->b - (int)c2->b) * ((int)c1->b - (int)c2->b);
	temp += ((int)c1->g - (int)c2->g) * ((int)c1->g - (int)c2->g);
	temp += ((int)c1->r - (int)c2->r) * ((int)c1->r - (int)c2->r);
	return temp;
}

int change_color(color_type* c1, color_type* listPtr, int list_len)
{
	long temp = 0;
	long temp_min = 0;
	unsigned char item_id = 0;
	color_type* list_temp = listPtr;
	int i;
	for (i = 0; i < list_len; i++)
	{
		temp = dis_tens_color(c1,listPtr + i);
		if (i == 0)
		{
			temp_min = temp;
			list_temp = listPtr + i;
			item_id = i;
		}
		else
		{
			if (temp < temp_min)
			{
				list_temp = listPtr + i;
				temp_min = temp;
				item_id = i;
			}
		}
	}
	c1->b = list_temp->b;
	c1->g = list_temp->g;
	c1->r = list_temp->r;
	return item_id;
}


int img_closePick(unsigned char* imgPtr,unsigned char * listPtr,unsigned char * pix_ptr,unsigned char * arg_ptr)
{
	arg_type * arg =(arg_type*)arg_ptr;
	long pix_number;
	unsigned char item_id = 0;
	for (pix_number = 0; pix_number < arg->pix_len; pix_number++)
	{
		item_id=change_color((color_type*)(imgPtr)+pix_number,(color_type*)listPtr, arg->list_len);
		*(pix_ptr + pix_number) = item_id;
	}
	return 0;
}


int img_not(unsigned char* imgPtr, unsigned char* mask,unsigned char* arg_ptr)
{
	long img_len =*((long*)arg_ptr);
	long i;
	for (i = 0; i < img_len; i++)
	{
		if (*(mask + i) == 255)
			if (*(imgPtr + i) == 255)
				*(imgPtr + i) = 0;
			else
				*(imgPtr + i) = 255;
	}
	return 0;
}

unsigned char repic_color(color_type* c1, color_type* listPtr)
{
	color_type* list_temp = listPtr;
	unsigned char item_id = 0;
	if (c1->b == 0)
	{
		list_temp = listPtr;
		item_id = 0;
	}
	else
	{
		list_temp = listPtr+1;
		item_id = 1;
	}

	c1->b = list_temp->b;
	c1->g = list_temp->g;
	c1->r = list_temp->r;
	return item_id;
}



int img_2pick(unsigned char* imgPtr, unsigned char* listPtr, unsigned char* pix_ptr, unsigned char* arg_ptr)
{
	arg_type* arg = (arg_type*)arg_ptr;
	long pix_number;
	unsigned char item_id = 0;
	for (pix_number = 0; pix_number < arg->pix_len; pix_number++)
	{
		item_id = repic_color((color_type*)(imgPtr)+pix_number, (color_type*)listPtr);
		*(pix_ptr + pix_number) = item_id;
	}
	return 0;
}

int my_pross(unsigned char* imgPtr, unsigned char* colorPtr,unsigned char* arg_ptr)
{
	color_type* img = (color_type*)(imgPtr);
	color_type* color = (color_type*)(colorPtr);
	long* arg = (long*)arg_ptr;
	long y = *arg;
	long x = *(arg+1);
	long cmp = *(arg+2);
	long i, j;
		for (i = 0; i < x; i++) {
			for (j = 0; j < y; j++) {
				if (j < cmp)
				{
					(img + i* y +  j)->b = color->b;
					(img + i * y + j)->g = color->g;
					(img + i * y + j)->r = color->r;
				}
				else
				{
					(img + i * y + j)->b = (color + 1)->b;
					(img + i * y + j)->g = (color + 1)->g;
					(img + i * y + j)->r = (color + 1)->r;
				}
			}
		}
		return 0;
}